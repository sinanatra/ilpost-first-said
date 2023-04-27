<script>
	import Viz from '../components/Viz.svelte';
	// import { articleData } from './store';

	// export let data;
	// let posts = data.posts;
	// let articleIndex = 0;

	// $articleData = posts[0];

	// function nextArticle() {
	// 	articleIndex = (articleIndex + 1) % posts.length;
	// 	$articleData = posts[articleIndex];
	// }
</script>

<!-- {#if data} -->
<section class="container">
	<Viz />
	<!-- <button on:click={nextArticle}>Next Article</button> -->
</section>

<!-- {/if} -->

<style>
	:global(body) {
		margin: 0;
	}
</style>
