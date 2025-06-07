#!/usr/bin/env node
/**
 * Enhanced API caller with authentication support
 * Supports various auth methods and credential loading
 */

const fs = require('fs');
const path = require('path');

// Load environment variables from .env file
function loadEnv() {
  const envPath = path.join(__dirname, '.env');
  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    envContent.split('\n').forEach(line => {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
        const [key, ...valueParts] = trimmed.split('=');
        const value = valueParts.join('=').replace(/^["']|["']$/g, '');
        process.env[key.trim()] = value;
      }
    });
  }
}

// Load environment variables
loadEnv();

(async () => {
  try {
    const stdin = await new Promise((resolve) => {
      let data = '';
      process.stdin.on('data', chunk => data += chunk);
      process.stdin.on('end', () => resolve(data));
    });

    const input = JSON.parse(stdin);
    const { url, auth_type, headers = {} } = input;

    // Add authentication headers based on type
    const requestHeaders = { ...headers };

    switch (auth_type) {
      case 'bearer':
        if (process.env.API_TOKEN) {
          requestHeaders['Authorization'] = `Bearer ${process.env.API_TOKEN}`;
        }
        break;
      
      case 'facebook':
        if (process.env.FACEBOOK_ACCESS_TOKEN) {
          requestHeaders['Authorization'] = `Bearer ${process.env.FACEBOOK_ACCESS_TOKEN}`;
        }
        break;
      
      case 'api_key':
        if (process.env.API_KEY) {
          requestHeaders['X-API-Key'] = process.env.API_KEY;
        }
        break;
      
      case 'custom':
        // Allow custom headers from input
        Object.assign(requestHeaders, input.custom_headers || {});
        break;
    }

    // Make the request
    const response = await fetch(url, {
      method: input.method || 'GET',
      headers: requestHeaders,
      body: input.body ? JSON.stringify(input.body) : undefined
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(JSON.stringify({
      success: true,
      data: data,
      status: response.status
    }));
    
  } catch (error) {
    console.log(JSON.stringify({ 
      success: false,
      error: error.message,
      type: error.constructor.name 
    }));
  }
})();