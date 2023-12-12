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
    }).sort({ _id: -1 }).toArray();



    // REMOVES STUFFFF
    // await db.collection('words').find({
    //     _id: {
    //         $gte: new ObjectId(Math.floor(start.getTime() / 1000).toString(16) + "0000000000000000"),
    //         $lt: new ObjectId(Math.floor(end.getTime() / 1000).toString(16) + "0000000000000000")
    //     }
    // }).sort({ _id: -1 }).limit(200).forEach(doc => db.collection('words').deleteOne({ _id: doc._id }))


    const data = await res.map(({ word, date_added, url, context, _id }) => ({ word, date_added, url, context, _id }));
    return new Response(JSON.stringify(data), { status: 200 });
}