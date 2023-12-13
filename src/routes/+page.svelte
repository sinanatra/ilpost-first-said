<script>
	import Viz from '../components/Viz.svelte';

	let sortingOption = 'Time';
	function handleSortingChange(event) {
		sortingOption = event.target.value;
	}
</script>

<svelte:head>
	<title>Nuove Parole Del Post</title>
	<meta name="title" content="Nuove Parole Del Post" />
	<meta
		name="description"
		content="Questa visualizzazione mostra le parole che sono state citate per la prima volta sul quotidiano ilPost negli ultimi 30 giorni."
	/>

	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://ilpostdice.giacomo.website/" />
	<meta property="og:title" content="Nuove Parole Del Post" />
	<meta
		property="og:description"
		content="Questa visualizzazione mostra le parole che sono state citate per la prima volta sul quotidiano ilPost negli ultimi 30 giorni."
	/>
	<meta property="og:image" content="cover.png" />

	<meta property="twitter:card" content="summary_large_image" />
	<meta property="twitter:url" content="https://ilpostdice.giacomo.website/" />
	<meta property="twitter:title" content="Nuove Parole Del Post" />
	<meta
		property="twitter:description"
		content="Questa visualizzazione mostra le parole che sono state citate per la prima volta sul quotidiano ilPost negli ultimi 30 giorni."
	/>
	<meta property="twitter:image" content="cover.png" />
</svelte:head>
<section class="intro">
	<div class="large">
		Questa visualizzazione mostra le parole che sono state citate per la prima volta sul quotidiano <a
			href="https://www.ilpost.it/"
			target="_blank">ilPost</a
		>
		negli ultimi 30 giorni.
	</div>

	<div>
		<p>
			Ogni due ore uno script monitora il <a href="https://www.ilpost.it/feed/">feed Rss</a> del Post,
			apre ogni articolo, controlla ogni parola e nel caso non sia mai stata utilizzata, la salva in
			un Database.
		</p>
		<p>
			Potete vedere come funziona su <a
				target="_blank"
				href="https://github.com/sinanatra/ilpost-first-said">Github</a
			>.
			<br />
			Inizialmente pensato come Bot su
			<a target="_blank" href="https://twitter.com/ilpostdice">Twitter</a>, e poi su
			<a target="_blank" href="https://t.me/nuoveparoledelpost">Telegram</a>.
		</p>
	</div>
	<div>
		<p>
			Realizzato da <a target="_blank" href="https://giacomo.website/">Giacomo Nanni</a>.
		</p>
	</div>
	<div class="filters">
		<p>
			Ordine:
			<label>
				<input
					type="radio"
					id="Time"
					name="sortingOption"
					value="Time"
					bind:group={sortingOption}
				/>
				Temporale
			</label>
			<label>
				<input
					type="radio"
					id="Alphabetically"
					name="sortingOption"
					value="Alphabetically"
					bind:group={sortingOption}
				/>
				Alfabetico
			</label>
		</p>
	</div>
</section>

<Viz {sortingOption} />

<style>
	:global(body) {
		font-family: Georgia, 'Times New Roman', Times, serif;
		--color-1: #2da8c6;
		-webkit-font-smoothing: antialiased;
		text-rendering: optimizeLegibility;
		margin: 0;
		padding: 0;
	}

	:global(::selection) {
		background-color: yellow;
	}

	a {
		color: var(--color-1);
	}

	p {
		margin-top: 5px;
		margin-bottom: 5px;
	}

	.intro {
		display: flex;
		flex-wrap: wrap;
		gap: 10px;
		padding: 5px;
		margin-bottom: 10px;
		border-bottom: 1px solid;
	}

	div {
		min-width: 300px;
		font-size: 12px;
		flex: 1;
	}

	.large {
		flex: 3;
		font-size: clamp(24px, 3vw, 3vw);
		line-height: clamp(24px, 2.9vw, 2.9vw);
	}

	.filters,
	.filters * {
		flex-basis: 100%;
		cursor: pointer;
		user-select: none;
	}

	input[type='radio'] {
		/* accent-color: var(--color-1); */
	}
</style>
