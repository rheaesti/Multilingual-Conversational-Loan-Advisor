<script>
    // Form data
    let formData = {
      fullName: '',
      address: '',
      phoneNo: '',
      aadharNo: '',
      gender: '',
      age: '',
      email: '',
      comments: ''
    };
  
    // Form submission handler
    function handleSubmit() {
      alert('Form submitted successfully!');
      console.log(formData);
    }
  
    // Reset form
    function resetForm() {
      formData = {
        fullName: '',
        address: '',
        phoneNo: '',
        aadharNo: '',
        gender: '',
        age: '',
        email: '',
        comments: ''
      };
    }
  
    // Help button handler
    function showHelp() {
      alert('Fill out all fields and click Submit. For assistance, contact support.');
    }
  
    // Window control handlers
    function minimizeWindow() {
      alert('Minimize functionality would be implemented in a desktop application');
    }
  
    function closeWindow() {
      if (confirm('Are you sure you want to close this form? Any unsaved data will be lost.')) {
        resetForm();
        alert('Close functionality would be implemented in a desktop application');
      }
    }
  
    // Input validation handlers
    function validatePhoneNumber(event) {
      // Allow only numbers and limit to 10 digits
      formData.phoneNo = event.target.value.replace(/[^0-9]/g, '').substring(0, 10);
    }
  
    function validateAadharNumber(event) {
      // Allow only numbers and limit to 12 digits
      formData.aadharNo = event.target.value.replace(/[^0-9]/g, '').substring(0, 12);
    }
  </script>
  
  <main>
    <div class="form-window">
      <div class="window-header">
        <div class="window-title">Loan Application Form</div>
        <div class="window-controls">
          <button type="button" class="window-button minimize" on:click={minimizeWindow}>_</button>
          <button type="button" class="window-button close" on:click={closeWindow}>×</button>
        </div>
      </div>
      
      <div class="window-content">
        <form on:submit|preventDefault={handleSubmit}>
          <div class="form-section">
            <div class="form-group">
              <label for="fullName">Full Name:</label>
              <input type="text" id="fullName" bind:value={formData.fullName} placeholder="Enter your full name" />
            </div>
            
            <div class="form-group">
              <label for="address">Address:</label>
              <textarea id="address" bind:value={formData.address} placeholder="Enter your complete address"></textarea>
            </div>
            
            <div class="form-group">
              <label for="phoneNo">Phone No:</label>
              <input 
                type="tel" 
                id="phoneNo" 
                bind:value={formData.phoneNo} 
                on:input={validatePhoneNumber}
                placeholder="Enter 10-digit number" 
              />
            </div>
            
            <div class="form-group">
              <label for="aadharNo">Aadhar No:</label>
              <input 
                type="text" 
                id="aadharNo" 
                bind:value={formData.aadharNo} 
                on:input={validateAadharNumber}
                placeholder="Enter 12-digit Aadhar number" 
              />
            </div>
            
            <div class="form-group radio-group">
              <label>Gender:</label>
              <div class="radio-options">
                <label class="radio-label">
                  <input type="radio" name="gender" value="Male" bind:group={formData.gender} />
                  <span>Male</span>
                </label>
                <label class="radio-label">
                  <input type="radio" name="gender" value="Female" bind:group={formData.gender} />
                  <span>Female</span>
                </label>
                <label class="radio-label">
                  <input type="radio" name="gender" value="Other" bind:group={formData.gender} />
                  <span>Other</span>
                </label>
              </div>
            </div>
            
            <div class="form-group">
              <label for="age">Age:</label>
              <input type="number" id="age" bind:value={formData.age} placeholder="Enter your age" />
            </div>
            
            <div class="form-group">
              <label for="email">Email:</label>
              <input type="email" id="email" bind:value={formData.email} placeholder="Enter your email address" />
            </div>
          </div>
          
          <div class="textbox-section">
            <label for="comments">Additional Comments:</label>
            <textarea id="comments" bind:value={formData.comments} placeholder="Any additional information you'd like to share..."></textarea>
          </div>
          
          <div class="button-row">
            <button type="submit" class="submit-button">Submit</button>
            <button type="button" class="reset-button" on:click={resetForm}>Reset</button>
            <button type="button" class="help-button" on:click={showHelp}>Help</button>
          </div>
        </form>
      </div>
    </div>
  </main>
  
  <style>
    /* Global styles */
    :global(*) {
      box-sizing: border-box;
      font-family: "MS Sans Serif", Arial, sans-serif;
      color: #000000;
    }
    
    :global(body) {
      margin: 0;
      padding: 0;
    }
    
    main {
      background-color: #ffff99;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }
    
    .form-window {
      width: 600px;
      background-color: #cccccc;
      border: 2px solid #000000;
      box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);
    }
    
    .window-header {
      background-color: #00CCCC;
      padding: 5px 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: bold;
    }
    
    .window-title {
      color: #000000;
    }
    
    .window-controls {
      display: flex;
      gap: 5px;
    }
    
    .window-button {
      width: 20px;
      height: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #cccccc;
      border: 1px outset #ffffff;
      cursor: pointer;
      font-size: 10px;
      padding: 0;
      color: #000000;
    }
    
    .window-content {
      padding: 15px;
    }
    
    form {
      display: flex;
      flex-direction: column;
      gap: 15px;
    }
    
    .form-section {
      display: flex;
      flex-direction: column;
      gap: 10px;
      padding-bottom: 15px;
      border-bottom: 2px groove #ffffff;
    }
    
    .form-group {
      margin-bottom: 5px;
    }
    
    label {
      display: block;
      margin-bottom: 3px;
      font-weight: bold;
      color: #000000;
    }
    
    input, textarea, select {
      width: 100%;
      padding: 5px;
      border: 2px inset #888888;
      background-color: #ffffff;
      font-size: 14px;
      color: #000000;
    }
    
    input::placeholder, textarea::placeholder {
      color: #666666;
    }
    
    textarea {
      min-height: 60px;
      resize: vertical;
    }
    
    #comments {
      min-height: 100px;
    }
    
    .radio-group {
      margin-bottom: 10px;
    }
    
    .radio-options {
      display: flex;
      gap: 20px;
    }
    
    .radio-label {
      display: flex;
      align-items: center;
      gap: 5px;
      font-weight: normal;
      color: #000000;
    }
    
    .radio-label input {
      width: auto;
      margin: 0;
    }
    
    .radio-label span {
      color: #000000;
    }
    
    .textbox-section {
      margin-bottom: 10px;
    }
    
    .button-row {
      display: flex;
      gap: 10px;
      justify-content: flex-end;
    }
    
    button {
      padding: 6px 15px;
      cursor: pointer;
      border: 2px outset #ffffff;
      color: #000000;
    }
    
    .submit-button {
      background-color: #00CCCC;
      font-weight: bold;
    }
    
    .reset-button {
      background-color: #cccccc;
    }
    
    .help-button {
      background-color: #cccccc;
    }
    
    button:active {
      border-style: inset;
    }
    
    /* Pixelated effect for retro feel */
    .form-window,
    button,
    input,
    textarea {
      image-rendering: -webkit-optimize-contrast;
      image-rendering: -moz-crisp-edges;
      image-rendering: -o-pixelated;
      image-rendering: pixelated;
      -ms-interpolation-mode: nearest-neighbor;
    }
    
    /* Responsive styling */
    @media screen and (max-width: 640px) {
      .form-window {
        width: 100%;
      }
      
      .radio-options {
        flex-direction: column;
        gap: 10px;
      }
    }
  </style>