const express = require('express');
const { MongoClient } = require('mongodb');
const path = require('path');

const app = express();
const port = 3000;

// Set EJS as the templating engine
app.set('view engine', 'ejs');

// MongoDB connection URL and database/collection names
const url = 'mongodb://localhost:27017';
const dbName = 'companyFinance';

// Route to display items
app.get('/', async (req, res) => {
    let client;

    try {
        client = await MongoClient.connect(url);
        const db = client.db(dbName);

        // Fetch the list of collections (industries)
        const collections = await db.listCollections().toArray();
        const industries = collections.map(col => col.name);

        // Fetch the selected industry from query parameters
        const selectedIndustry = req.query.industry || industries[0];
        const collection = db.collection(selectedIndustry);

        // Fetch distinct sectors
        const sectors = await collection.distinct('Industry');

        // Fetch the selected sector from query parameters
        const selectedSector = req.query.sector || sectors[0];

        // Fetch the top 20 items sorted by Industry and then by Revenue ($B) in descending order for the selected sector
        const items = await collection.find({ Industry: selectedSector })
            .sort({ Industry: 1, "Income.Revenue ($B)": -1 })
            .limit(20)
            .toArray();

        res.render('index', { items, industries, selectedIndustry, sectors, selectedSector }); // Pass items, industries, selected industry, sectors, and selected sector to the template
    } catch (err) {
        console.error('Error connecting to MongoDB or fetching data:', err);
        res.status(500).send('Internal Server Error');
    } finally {
        if (client) {
            client.close();
        }
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});