<script>
  import './styles.css'
    // States for tracking uploads
    let aadharFile = null;
    let panFile = null;
    let aadharPreview = '';
    let panPreview = '';
    let isUploading = false;
    let uploadProgress = 0;
    let showSuccess = false;
    let errorMessage = '';
    
    // Handle Aadhar file selection
    function handleAadharChange(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      aadharFile = file;
      const reader = new FileReader();
      reader.onload = e => {
        aadharPreview = e.target.result;
      };
      reader.readAsDataURL(file);
    }
    
    // Handle PAN file selection
    function handlePanChange(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      panFile = file;
      const reader = new FileReader();
      reader.onload = e => {
        panPreview = e.target.result;
      };
      reader.readAsDataURL(file);
    }
    
    // Submit the files
    function handleSubmit() {
      if (!aadharFile && !panFile) {
        errorMessage = "Please upload at least one document";
        return;
      }
      
      errorMessage = "";
      isUploading = true;
      
      // Simulate upload progress
      const interval = setInterval(() => {
        uploadProgress += 5;
        if (uploadProgress >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            isUploading = false;
            showSuccess = true;
          }, 500);
        }
      }, 200);
    }
    
    // Reset the form
    function resetForm() {
      aadharFile = null;
      panFile = null;
      aadharPreview = '';
      panPreview = '';
      isUploading = false;
      uploadProgress = 0;
      showSuccess = false;
      errorMessage = '';
    }
  </script>
  
  <main>
    <div class="title-bar">
      <div class="dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <h1>DOCUMENT UPLOADER</h1>
      <div class="close-btn">✕</div>
    </div>
    
    {#if showSuccess}
      <div class="window success-window">
        <div class="window-header">
          <div class="title">Success!</div>
          <div class="close-btn" on:click={resetForm}>✕</div>
        </div>
        <div class="window-content">
          <div class="icon">✓</div>
          <p>Your documents have been uploaded successfully!</p>
          <button class="retro-button" on:click={resetForm}>OK</button>
        </div>
      </div>
    {:else if isUploading}
      <div class="window progress-window">
        <div class="window-header">
          <div class="title">Please wait...</div>
        </div>
        <div class="window-content">
          <div class="progress-container">
            <div class="progress-bar" style="width: {uploadProgress}%"></div>
          </div>
          <div class="progress-text">{uploadProgress}% Complete</div>
        </div>
      </div>
    {:else}
      <div class="window-container">
        <div class="window upload-window">
          <div class="window-header">
            <div class="title">Upload Documents</div>
            <div class="window-controls">
              <span>_</span>
              <span>□</span>
              <span>✕</span>
            </div>
          </div>
          
          <div class="window-content">
            {#if errorMessage}
              <div class="error-message">
                <div class="error-icon">!</div>
                <p>Oops! {errorMessage}</p>
              </div>
            {/if}
            
            <div class="upload-section">
              <div class="document-type">
                <div class="icon-container">
                  <div class="document-icon">📄</div>
                </div>
                <h3>Aadhar Card</h3>
                
                <label class="file-input-container">
                  <input 
                    type="file" 
                    accept="image/*,.pdf" 
                    on:change={handleAadharChange}
                  />
                  <span class="retro-button">Select File</span>
                </label>
                
                {#if aadharPreview}
                  <div class="preview">
                    <div class="preview-header">
                      <span>Preview</span>
                      <button class="remove-btn" on:click={() => { aadharFile = null; aadharPreview = ''; }}>✕</button>
                    </div>
                    <div class="preview-content">
                      {#if aadharFile.type.includes('image')}
                        <img src={aadharPreview} alt="Aadhar Preview" />
                      {:else}
                        <div class="file-icon">📄 {aadharFile.name}</div>
                      {/if}
                    </div>
                  </div>
                {/if}
              </div>
              
              <div class="document-type">
                <div class="icon-container">
                  <div class="document-icon">🆔</div>
                </div>
                <h3>PAN Card</h3>
                
                <label class="file-input-container">
                  <input 
                    type="file" 
                    accept="image/*,.pdf" 
                    on:change={handlePanChange}
                  />
                  <span class="retro-button">Select File</span>
                </label>
                
                {#if panPreview}
                  <div class="preview">
                    <div class="preview-header">
                      <span>Preview</span>
                      <span class="remove-btn" on:click={() => { panFile = null; panPreview = ''; }}>✕</span>
                    </div>
                    <div class="preview-content">
                      {#if panFile.type.includes('image')}
                        <img src={panPreview} alt="PAN Preview" />
                      {:else}
                        <div class="file-icon">📄 {panFile.name}</div>
                      {/if}
                    </div>
                  </div>
                {/if}
              </div>
            </div>
            
            <div class="buttons-container">
              <button class="retro-button upload-btn" on:click={handleSubmit}>Upload Files</button>
              <button class="retro-button cancel-btn" on:click={resetForm}>Cancel</button>
            </div>
          </div>
        </div>
        
        <div class="footer">
          <div class="status-bar">
            <div class="status-item">Ready</div>
            <div class="status-item date">
              {new Date().toLocaleDateString()}
            </div>
          </div>
        </div>
      </div>
    {/if}
  </main>
  
 <style>
    :global(body) {
  margin: 0;
  font-family: 'VT323', monospace;
  background-color: #ffff99;
  color: #000;
  padding: 20px;
}
 </style>