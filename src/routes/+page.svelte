<script>
	import Menu from '../components/Menu.svelte';
	import Article from '../components/Article.svelte';
	import WordsContainer from '../components/WordsContainer.svelte';

	export let data;
	let posts = data.posts;
</script>

{#if data}
	<section class="container">
		<Menu {posts} />
		<Article article={data.posts[0]} />
		<WordsContainer />
	</section>
{/if}

<style>
    :global(body) {
        margin: 0;
    }
</style>
