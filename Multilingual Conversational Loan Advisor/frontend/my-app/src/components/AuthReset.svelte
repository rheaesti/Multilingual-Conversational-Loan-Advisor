<script>
	import { authHandlers, authStore } from '../stores/authStore';
    import './styles2.css'
	let action = '';
	let newEmail = '';
	let newPass = '';

	async function handleSubmit() {
		if (!action) {
			return;
		}

		if (action === 'updatePass') {
			return await authHandlers.updatePassword(newPass);
		}

		if (action === 'updateEmail') {
            console.log(newEmail)
			return await authHandlers.updateEmail(newEmail);
		}
	}
</script>

<div class="container">
	<div class="window">
		<div class="title-bar">
			<div class="title">Settings</div>
			<div class="controls">
				<button class="close">✕</button>
			</div>
		</div>
		<div class="window-content">
			<div class="action-buttons">
				<button
					class="option-btn {action === 'updateEmail' ? 'active' : ''}"
					on:click={() => {
						action = 'updateEmail';
					}}>Update Email</button
				>
				<button
					class="option-btn {action === 'updatePass' ? 'active' : ''}"
					on:click={() => {
						action = 'updatePass';
					}}>Update Password</button
				>
			</div>
			
			{#if action === 'updatePass'}
				<div class="form-container">
					<div class="input-group">
						<label>New Password:</label>
						<input bind:value={newPass} type="password" placeholder="New Password" />
					</div>
					<div class="button-group">
						<button class="submit-btn" on:click={handleSubmit}>OK</button>
						<button class="cancel-btn" on:click={() => action = ''}>Cancel</button>
					</div>
				</div>
			{/if}
			
			{#if action === 'updateEmail'}
				<div class="form-container">
					<div class="input-group">
						<label>New Email:</label>
						<input bind:value={newEmail} type="email" placeholder="New Email" />
					</div>
					<div class="button-group">
						<button class="submit-btn" on:click={handleSubmit}>OK</button>
						<button class="cancel-btn" on:click={() => action = ''}>Cancel</button>
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	:global(body) {
		background-color: #ffff99;
		font-family: 'Courier New', monospace;
	}
</style>