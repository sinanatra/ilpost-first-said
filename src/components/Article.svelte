<script>
	export let article;

	let words = article.content.replace(/<[^>]+>/g, '').match(/\b\w+\b|[^\s]/g);
</script>

<article>
	<h1>{article.title}</h1>
	<div>
		{#each words as word}
			<span>{word} </span>
		{/each}
	</div>
</article>

<style>
	article {
		font-size: 24px;
		max-width: 800px;
        word-wrap: break-word;
	}

	h1 {
		margin: 0;
		padding-bottom: 1rem;
	}

   
    span {
        background-color: #f0f0f0;
        padding: 0 .1rem;
    }
</style>
