async function getFeed(url) {
    const response = await fetch(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(url)}`);
    const data = await response.json();
    return data.items;
}

// export const load = async () => {
//     const posts = await getFeed('https://rss.draghetti.it/ilpost.xml');
//     return {
//         posts
//     };
// };
