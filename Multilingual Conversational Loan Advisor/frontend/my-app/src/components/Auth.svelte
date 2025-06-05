<script>
	import { authHandlers, authStore } from '../Stores/authstore.js';
    import './styles.css'
	let register = false;
	let email = '';
	let password = '';
	let confirmPassword = '';
	let processing = false;
	let errorMessage = '';

	async function handleSubmit() {
		if (!email || !password || (register && !confirmPassword)) {
			errorMessage = 'ERROR!!! All fields required';
			return;
		}

		if (register && password !== confirmPassword) {
			errorMessage = 'ERROR!!! Passwords do not match';
			return;
		}

		processing = true;
		errorMessage = '';
		
		try {
			if (register) {
				await authHandlers.signup(email, password);
			} else {
				await authHandlers.login(email, password);
			}
			
			if ($authStore.currentUser) {
				window.location.href = '/Chatbot';
			} else {
				errorMessage = 'ERROR!!! Authentication failed';
			}
		} catch (err) {
			console.log(err);
			errorMessage = `ERROR!!! ${err.message || 'Something went wrong'}`;
		} finally {
			processing = false;
		}
	}
</script>

<div class="container">
	<div class="bank-header">
		<div class="bank-logo">
			<div class="bank-icon">🏦</div>
			<div class="bank-text">BANK TERMINAL</div>
		</div>
	</div>

	<div class="window">
		<div class="title-bar">
			<div class="title-dots">
				{#each Array(20) as _, i}
					<span class="dot">·</span>
				{/each}
			</div>
			<div class="title">{register ? 'NEW ACCOUNT' : 'ACCESS TERMINAL'}</div>
			<div class="title-dots">
				{#each Array(20) as _, i}
					<span class="dot">·</span>
				{/each}
			</div>
			<div class="controls">
				<button class="control minimize">_</button>
				<button class="control maximize">□</button>
				<button class="control close">✕</button>
			</div>
		</div>

		<div class="window-content">
			{#if errorMessage}
				<div class="error-box">
					<div class="error-icon">⚠️</div>
					<div class="error-message">{errorMessage}</div>
					<button class="error-close" on:click={() => errorMessage = ''}>OK</button>
				</div>
			{/if}

			{#if processing}
				<div class="processing-box">
					<div class="processing-title">PLEASE WAIT...</div>
					<div class="progress-bar">
						<div class="progress-fill"></div>
					</div>
					<div class="processing-text">PROCESSING REQUEST</div>
				</div>
			{:else}
				<form on:submit|preventDefault={handleSubmit}>
					<div class="input-group">
						<label>USER ID:</label>
						<input bind:value={email} type="email" placeholder="Enter email address" />
					</div>
					<div class="input-group">
						<label>PASSCODE:</label>
						<input bind:value={password} type="password" placeholder="Enter secure passcode" />
					</div>
					{#if register}
						<div class="input-group">
							<label>CONFIRM:</label>
							<input bind:value={confirmPassword} type="password" placeholder="Verify secure passcode" />
						</div>
					{/if}
					
					<div class="button-row">
						<button type="submit" class="action-btn">SUBMIT</button>
					</div>
				</form>
				
				<div class="action-buttons">
					{#if register}
						<button type="button" class="link-btn" on:click={() => { register = false; }}>
							→ EXISTING ACCOUNT LOGIN
						</button>
					{:else}
						<button type="button" class="link-btn" on:click={() => { register = true; }}>
							→ NEW ACCOUNT REGISTRATION
						</button>
						<button type="button" class="link-btn" on:click={() => authHandlers.resetPassword(email)}>
							→ PASSCODE RECOVERY
						</button>
					{/if}
				</div>
			{/if}
		</div>
		
		<div class="status-bar">
			<div class="status-item">SECURE CONNECTION</div>
			<div class="status-item blink">READY</div>
			<div class="status-item">V 1.0.4</div>
		</div>
	</div>
</div>

<style>
    :global(body) {
    background-color: #ffff99;
    font-family: 'Courier New', monospace;
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
}
</style>