<script>
	import Chat from "./Chatbot.svelte";
</script>

<main>
	<Chat/>
</main>

<style>
	* {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	@media (max-width: 1024px) {
		main {
			width: 95%;
			padding: 20px;
		}
	}

	@media (max-width: 768px) {
		main {
			flex-direction: column;
			padding: 10px;
		}
	}
</style>