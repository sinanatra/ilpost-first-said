import db from "$lib/db";

const now = new Date();
const romeTimeString = now.toLocaleString('en-US', { timeZone: 'Europe/Rome' });
const romeTime = new Date(romeTimeString);

const start = new Date(romeTime - 30 * 24 * 60 * 60 * 1000); // 30 days ago
const end = romeTime;

export const GET = async ({ request, url }) => {
    const res = await db.collection('words').find({
        date_added: {
            $exists: true,
            $gte: start.toISOString(),
            $lt: end.toISOString()
        },
        word: {
            $regex: /\w{4,}/ // Match words with length greater than 3
        },
        url: { $exists: true },
        context: { $exists: true }
    }).sort({ date_added: -1 }).toArray();


    const data = await res.map(({ word, date_added, url, context, _id }) => ({ word, date_added, url, context, _id }));
    return new Response(JSON.stringify(data), { status: 200 });
}