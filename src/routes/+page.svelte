<script>
	import Menu from '../components/Menu.svelte';
	import Viz from '../components/Viz.svelte';
	import WordsContainer from '../components/WordsContainer.svelte';

	export let data;
	let posts = data.posts;
    console.log(posts)
</script>

{#if data}
	<section class="container">
		<Menu {posts} />
		<Viz article={data.posts[0]} />
		<WordsContainer />
	</section>
{/if}

<style>
    :global(body) {
        margin: 0;
    }
</style>
