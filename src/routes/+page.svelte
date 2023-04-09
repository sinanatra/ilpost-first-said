<script>
	import Menu from '../components/Menu.svelte';
	import Viz from '../components/Viz.svelte';
	import WordsContainer from '../components/WordsContainer.svelte';
	import { articleData } from './store';

	export let data;
	let posts = data.posts;

	let articleIndex = 0;

	$articleData = posts[0];

	function nextArticle() {
		articleIndex = (articleIndex + 1) % posts.length;
		$articleData = posts[articleIndex];
	}
</script>

{#if data}
	<section class="container">
		<h1>
			{posts[articleIndex].title}
		</h1>

		<button on:click={nextArticle}>Next Article</button>
		<Viz />

		<WordsContainer />
	</section>
{/if}

<style>
	:global(body) {
		margin: 0;
	}
</style>
