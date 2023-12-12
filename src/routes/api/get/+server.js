import db from "$lib/db"
import { ObjectId } from 'mongodb';

const now = new Date();
const start = new Date(now - 150 * 24 * 60 * 60 * 1000); // 30 days ago
const end = now;

export const GET = async ({ request, url }) => {

    const res = await db.collection('words').find({
        _id: {
            $gte: new ObjectId(Math.floor(start.getTime() / 1000).toString(16) + "0000000000000000"),
            $lt: new ObjectId(Math.floor(end.getTime() / 1000).toString(16) + "0000000000000000")
        }
    }).toArray();

    const data = await res.map(({ word, date_added, url, context }) => ({ word, date_added, url, context }));
    return new Response(JSON.stringify(data), { status: 200 });
}