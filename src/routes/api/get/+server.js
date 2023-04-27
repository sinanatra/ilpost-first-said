import db from "$lib/db"
import { ObjectId } from 'mongodb';

const now = new Date();
const start = new Date(now - 668 * 60 * 60 * 1000);
const end = now;

export const GET = async ({ request, url }) => {

    const res = await db.collection('words').find({
        _id: {
            $gte: new ObjectId(Math.floor(start.getTime() / 1000).toString(16) + "0000000000000000"),
            $lt: new ObjectId(Math.floor(end.getTime() / 1000).toString(16) + "0000000000000000")
        }
    }).toArray();

    const data = await res.map(({ word }) => word); 
    return new Response(JSON.stringify(data), { status: 200 });
}