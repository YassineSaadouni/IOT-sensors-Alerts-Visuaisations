import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-kibana-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard-container">
      <div class="dashboard-header">
        <h2>📊 Tableaux de bord Kibana</h2>
        <p class="header-subtitle">Intégrez vos iframes Kibana ci-dessous</p>
      </div>

      <!-- Section Overview -->
      <div class="iframe-section">
        <div class="section-header">
          <h3>🏠 Vue d'ensemble</h3>
          <span class="section-badge">Dashboard 1</span>
        </div>
        <div class="iframe-placeholder">
          <!-- AJOUTEZ VOTRE IFRAME OVERVIEW ICI -->
          <div class="placeholder-content">
            <p class="placeholder-instructions">
<iframe src="http://localhost:5601/app/dashboards#/view/38ed7e10-d461-11f0-b7e9-5150dc613157?embed=true&_g=()&show-time-filter=true" height="1200" width="1200"></iframe>            </p>
          </div>
        </div>
      </div>
   </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 2rem;
      max-width: 1400px;
      margin: 0 auto;
      background: #f5f7fa;
      min-height: 100vh;
    }
    
    .dashboard-header {
      text-align: center;
      margin-bottom: 3rem;
      padding: 2rem;
      background: white;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .dashboard-header h2 {
      margin: 0 0 0.5rem 0;
      color: #2d3748;
      font-size: 2rem;
    }

    .header-subtitle {
      color: #718096;
      font-size: 1.1rem;
      margin: 0;
    }

    .iframe-section {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 2rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      padding-bottom: 1rem;
      border-bottom: 2px solid #e2e8f0;
    }

    .section-header h3 {
      margin: 0;
      color: #2d3748;
      font-size: 1.5rem;
    }

    .section-badge {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: 600;
    }

    .iframe-placeholder {
      min-height: 600px;
      border: 3px dashed #cbd5e0;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f7fafc;
      position: relative;
    }

    .placeholder-content {
      text-align: center;
      padding: 2rem;
    }

    .placeholder-icon {
      font-size: 4rem;
      margin-bottom: 1rem;
      opacity: 0.6;
    }

    .placeholder-title {
      font-size: 1.5rem;
      font-weight: 600;
      color: #4a5568;
      margin-bottom: 1rem;
    }

    .placeholder-instructions {
      color: #718096;
      font-size: 1rem;
      line-height: 1.6;
      margin: 0;
    }

    .usage-guide {
      background: white;
      border-radius: 12px;
      padding: 2rem;
      margin-top: 3rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      border-left: 4px solid #667eea;
    }

    .usage-guide h4 {
      margin-top: 0;
      color: #2d3748;
      font-size: 1.3rem;
    }

    .usage-guide ol {
      color: #4a5568;
      line-height: 1.8;
      padding-left: 1.5rem;
    }

    .usage-guide li {
      margin-bottom: 0.75rem;
    }

    .usage-guide a {
      color: #667eea;
      text-decoration: none;
      font-weight: 600;
    }

    .usage-guide a:hover {
      text-decoration: underline;
    }

    .usage-guide code {
      background: #edf2f7;
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      font-family: 'Courier New', monospace;
      color: #e53e3e;
      font-size: 0.9rem;
    }

    .example-code {
      background: #2d3748;
      color: #e2e8f0;
      padding: 1.5rem;
      border-radius: 8px;
      margin-top: 1rem;
      overflow-x: auto;
    }

    .example-code strong {
      color: #48bb78;
      display: block;
      margin-bottom: 0.5rem;
    }

    .example-code pre {
      margin: 0;
      font-family: 'Courier New', monospace;
      font-size: 0.9rem;
      line-height: 1.6;
      color: #a0aec0;
    }

    /* Style pour les iframes quand vous les ajouterez */
    .kibana-iframe {
      width: 100%;
      height: 600px;
      border: none;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    
      display: inline-block;
      font-size: 0.9rem;
    }
    
    .btn-refresh {
      background: #007bff;
      color: white;
    }
    
    .btn-refresh:hover {
      background: #0056b3;
    }
    
    .btn-external {
      background: #28a745;
      color: white;
    }
    
    .btn-external:hover {
      background: #218838;
    }
    
    .dashboard-selector {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin: 0 1rem;
    }
    
    .dashboard-selector button {
      padding: 0.5rem 1rem;
      border: 2px solid #ddd;
      background: white;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.3s;
      font-size: 0.85rem;
    }
    
    .dashboard-selector button:hover {
      background: #f0f0f0;
      border-color: #007bff;
    }
    
    .dashboard-selector button.active {
      background: #007bff;
      color: white;
      border-color: #007bff;
      font-weight: bold;
    }
    
    .dashboard-content {
      flex: 1;
      position: relative;
      overflow: hidden;
    }
    
    .kibana-iframe {
      width: 100%;
      height: 100%;
      border: none;
    }
    
    .loading-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(255, 255, 255, 0.9);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
    
    .spinner {
      border: 4px solid #f3f3f3;
      border-top: 4px solid #007bff;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `]
})
export class KibanaDashboardComponent implements OnInit {
  // Ce composant est prêt pour recevoir vos iframes Kibana
  // Vous pouvez ajouter vos propres méthodes et propriétés ici si nécessaire
  
  constructor() {}

  ngOnInit() {
    console.log('Kibana Dashboard Component initialisé');
    console.log('Prêt à recevoir vos iframes!');
  }
}
