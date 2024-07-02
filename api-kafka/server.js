const express = require('express');
const { Kafka } = require('kafkajs');

const app = express();
const port = 3001;

const kafka = new Kafka({
  clientId: 'my-api',
  brokers: ['localhost:9092']
});

const consumer = kafka.consumer({ groupId: 'group-id' });

const runConsumer = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'nom_du_topic', fromBeginning: true });
  app.get('/data', async (req, res) => {
    let messages = [];
    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        messages.push({
          value: message.value.toString(),
        });
        if (messages.length >= 10) {
          consumer.pause([{ topic }]);
          res.json(messages);
          messages = [];
        }
      },
    });
  });
};

runConsumer().catch(console.error);

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});