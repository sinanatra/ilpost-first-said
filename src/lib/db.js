import { MongoClient } from "mongodb"
import { DB_URI } from '$env/static/private';

const client = new MongoClient(DB_URI)
await client.connect()
export default client.db('ilpost') 