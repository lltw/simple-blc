db = db.getSiblingDB("test_mongodb");

db.user_submitted_data.drop();

db.user_submitted_data.insertMany([
    {
        id: 1,
        name: "Alice",
        type: "wild"
    },
    {
        id: 2,
        name: "Bob",
        type: "domestic"
    },
]);