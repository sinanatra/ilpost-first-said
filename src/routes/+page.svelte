<script>
	import Viz from '../components/Viz.svelte';

	let sortingOption = 'Time';
	function handleSortingChange(event) {
		sortingOption = event.target.value;
	}
</script>

<section class="intro">
	<div class="large">
		Questa visualizzazione mostra le parole che sono state citate per la prima volta sul quotidiano <a
			href="https://www.ilpost.it/"
			target="_blank">ilPost</a
		>
		negli ultimi 30 giorni.
		<div class="filters">
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
		</div>
	</div>

	<div>
		Potete vedere come funziona su <a
			target="_blank"
			href="https://github.com/sinanatra/ilpost-first-said">Github</a
		>. 
		<br>
		Inizialmente pensato come Bot su
		<a target="_blank" href="https://twitter.com/ilpostdice">Twitter</a>, e per
		<a target="_blank" href="https://t.me/nuoveparoledelpost">Telegram</a>
	</div>
	<div>Realizzato da <a target="_blank" href="https://giacomo.website/">Giacomo Nanni</a></div>
</section>
<Viz {sortingOption} />

<style>
	:global(body) {
		font-family: Georgia, 'Times New Roman', Times, serif;
		-webkit-font-smoothing: antialiased;
		text-rendering: optimizeLegibility;
		margin: 0;
		padding: 0;
	}

	:global(::selection) {
		background-color: yellow;
	}

	a {
		color: #2da8c6;
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
		font-size: 12px;
		flex: 1;
	}

	.large {
		flex: 3;
		font-size: clamp(24px, 3vw, 3vw);
		line-height: clamp(24px, 2.8vw, 2.8vw);
	}

	.filters,
	.filters * {
		cursor: pointer;
		user-select: none;
	}

	 input[type=radio]{
		/* accent-color: #2da8c6; */
	}
</style>
