import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ElasticsearchSearchService, SearchResult } from './services/elasticsearch-search.service';

@Component({
  selector: 'app-kibana-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="dashboard-container">
      <div class="dashboard-header">
        <h2>📊 Tableaux de bord IoT</h2>
        <p class="header-subtitle">Recherchez dans les données Elasticsearch ou consultez les dashboards Kibana</p>
      </div>

      <!-- Search Section -->
      <div class="search-section">
        <div class="search-header">
          <h3>🔍 Recherche Elasticsearch</h3>
        </div>
        
        <div class="search-controls">
          <div class="search-input-wrapper">
            <input 
              type="text" 
              class="search-input"
              [(ngModel)]="searchQuery"
              (keyup.enter)="performSearch()"
              placeholder="Rechercher dans les données... (capteurs, alertes, consommation, etc.)"
            />
            <button class="btn-search" (click)="performSearch()" [disabled]="isSearching">
              {{ isSearching ? '⏳ Recherche...' : '🔍 Rechercher' }}
            </button>
          </div>
          
          <div class="search-filters">
            <select class="filter-select" [(ngModel)]="selectedIndex" (change)="onIndexChange()">
              <option value="">Tous les indices</option>
              <option value="iot-alertes">Alertes</option>
              <option value="iot-capteurs">Capteurs IoT</option>
              <option value="iot-consommation">Consommation Énergie</option>
              <option value="iot-occupation">Occupation</option>
              <option value="iot-maintenance">Maintenance</option>
            </select>
            
            <select class="filter-select" [(ngModel)]="resultsPerPage">
              <option value="10">10 résultats</option>
              <option value="20">20 résultats</option>
              <option value="50">50 résultats</option>
              <option value="100">100 résultats</option>
            </select>
            
            <button class="btn-clear" (click)="clearSearch()" *ngIf="searchResults">
              ❌ Effacer
            </button>
          </div>
        </div>

        <!-- Search Results -->
        <div class="search-results" *ngIf="searchResults">
          <div class="results-header">
            <h4>Résultats de recherche</h4>
            <span class="results-count">{{ searchResults.total }} résultat(s) trouvé(s)</span>
          </div>
          
          <div class="error-message" *ngIf="searchResults.error">
            ⚠️ Erreur: {{ searchResults.error }}
          </div>
          
          <div class="results-list" *ngIf="searchResults.documents && searchResults.documents.length > 0">
            <div class="result-item" 
                 *ngFor="let doc of searchResults.documents; let i = index"
                 [class.top-result]="i < 3"
                 [class.top-1]="i === 0"
                 [class.top-2]="i === 1"
                 [class.top-3]="i === 2">
              
              <div class="result-header">
                <div class="header-left">
                  <span class="result-index" [class.top-badge]="i < 3">
                    <span *ngIf="i === 0">🥇</span>
                    <span *ngIf="i === 1">🥈</span>
                    <span *ngIf="i === 2">🥉</span>
                    <span *ngIf="i >= 3">{{ i + 1 }}</span>
                  </span>
                  <span class="result-score" *ngIf="doc._score">
                    ⭐ {{ doc._score | number:'1.2-2' }}
                  </span>
                </div>
                <span class="result-id">{{ doc._id }}</span>
              </div>

              <div class="result-preview">
                <div class="preview-field" *ngIf="doc.batiment">
                  <strong>🏢 Bâtiment:</strong> {{ doc.batiment }}
                </div>
                <div class="preview-field" *ngIf="doc.description">
                  <strong>📝 Description:</strong> {{ doc.description }}
                </div>
                <div class="preview-field" *ngIf="doc.type_alerte">
                  <strong>🚨 Type:</strong> {{ doc.type_alerte }}
                </div>
                <div class="preview-field" *ngIf="doc.severite">
                  <strong>⚠️ Sévérité:</strong> 
                  <span class="severity-badge" [class]="'severity-' + doc.severite">{{ doc.severite }}</span>
                </div>
                <div class="preview-field" *ngIf="doc.statut">
                  <strong>📊 Statut:</strong> {{ doc.statut }}
                </div>
                <div class="preview-field" *ngIf="doc.salle">
                  <strong>🚪 Salle:</strong> {{ doc.salle }}
                </div>
                <div class="preview-field" *ngIf="doc.zone">
                  <strong>📍 Zone:</strong> {{ doc.zone }}
                </div>
                <div class="preview-field" *ngIf="doc['@timestamp'] || doc.timestamp">
                  <strong>🕐 Date:</strong> {{ doc['@timestamp'] || doc.timestamp }}
                </div>
              </div>

              <div class="result-content" [class.expanded]="expandedResults[i]">
                <pre>{{ doc | json }}</pre>
              </div>
              
              <button class="btn-toggle" (click)="toggleResult(i)">
                {{ expandedResults[i] ? '▲ Masquer détails' : '▼ Voir tous les détails' }}
              </button>
            </div>
          </div>
          
          <div class="no-results" *ngIf="searchResults.documents && searchResults.documents.length === 0">
            <p>😕 Aucun résultat trouvé pour "{{ searchQuery }}"</p>
            <p class="hint">Essayez avec d'autres mots-clés ou changez le filtre d'index.</p>
          </div>
        </div>
      </div>

      <!-- Kibana Dashboard Section -->
      <div class="iframe-section">
        <div class="section-header">
          <h3>🏠 Vue d'ensemble Kibana</h3>
          <span class="section-badge">Dashboard Kibana</span>
        </div>
        <div class="iframe-placeholder">
          <div class="placeholder-content">
            <iframe 
              src="http://localhost:5601/app/dashboards#/view/38ed7e10-d461-11f0-b7e9-5150dc613157?embed=true&_g=()&show-time-filter=true" 
              height="1200" 
              width="1200"
              sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
              allow="fullscreen"
              loading="lazy">
            </iframe>
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
      margin-bottom: 2rem;
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

    /* Search Section Styles */
    .search-section {
      background: white;
      border-radius: 12px;
      padding: 2rem;
      margin-bottom: 2rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .search-header h3 {
      margin: 0 0 1.5rem 0;
      color: #2d3748;
      font-size: 1.5rem;
    }

    .search-controls {
      margin-bottom: 2rem;
    }

    .search-input-wrapper {
      display: flex;
      gap: 1rem;
      margin-bottom: 1rem;
    }

    .search-input {
      flex: 1;
      padding: 0.75rem 1rem;
      border: 2px solid #e2e8f0;
      border-radius: 8px;
      font-size: 1rem;
      transition: border-color 0.3s;
    }

    .search-input:focus {
      outline: none;
      border-color: #667eea;
    }

    .btn-search {
      padding: 0.75rem 2rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s;
    }

    .btn-search:hover:not(:disabled) {
      transform: translateY(-2px);
    }

    .btn-search:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .search-filters {
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
    }

    .filter-select {
      padding: 0.5rem 1rem;
      border: 2px solid #e2e8f0;
      border-radius: 8px;
      font-size: 0.9rem;
      background: white;
      cursor: pointer;
    }

    .btn-clear {
      padding: 0.5rem 1rem;
      background: #e53e3e;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 0.9rem;
      cursor: pointer;
      transition: background 0.3s;
    }

    .btn-clear:hover {
      background: #c53030;
    }

    /* Search Results Styles */
    .search-results {
      margin-top: 2rem;
      border-top: 2px solid #e2e8f0;
      padding-top: 2rem;
    }

    .results-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
    }

    .results-header h4 {
      margin: 0;
      color: #2d3748;
      font-size: 1.3rem;
    }

    .results-count {
      background: #48bb78;
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: 600;
    }

    .error-message {
      background: #fed7d7;
      color: #c53030;
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 1rem;
    }

    .results-list {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .result-item {
      background: #f7fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 1.5rem;
      transition: all 0.3s;
      position: relative;
    }

    .result-item:hover {
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      transform: translateY(-2px);
    }

    /* Top 3 Results Styling */
    .result-item.top-result {
      border-width: 2px;
    }

    .result-item.top-1 {
      background: linear-gradient(135deg, #fef3c7 0%, #fef9e7 100%);
      border-color: #f59e0b;
      box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }

    .result-item.top-2 {
      background: linear-gradient(135deg, #e5e7eb 0%, #f3f4f6 100%);
      border-color: #9ca3af;
      box-shadow: 0 4px 12px rgba(156, 163, 175, 0.3);
    }

    .result-item.top-3 {
      background: linear-gradient(135deg, #fed7aa 0%, #fde8d7 100%);
      border-color: #f97316;
      box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
    }

    .result-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      padding-bottom: 1rem;
      border-bottom: 2px solid #e2e8f0;
    }

    .header-left {
      display: flex;
      gap: 1rem;
      align-items: center;
    }

    .result-index {
      background: #667eea;
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 25px;
      font-weight: 700;
      font-size: 1.1rem;
      min-width: 50px;
      text-align: center;
    }

    .result-index.top-badge {
      font-size: 1.5rem;
      padding: 0.5rem 1.2rem;
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.05); }
    }

    .result-score {
      background: #48bb78;
      color: white;
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-weight: 600;
      font-size: 1rem;
    }

    .result-id {
      color: #718096;
      font-size: 0.85rem;
      font-family: monospace;
      background: #edf2f7;
      padding: 0.25rem 0.75rem;
      border-radius: 4px;
    }

    /* Preview Section */
    .result-preview {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 0.75rem;
      margin-bottom: 1rem;
    }

    .preview-field {
      background: white;
      padding: 0.75rem;
      border-radius: 6px;
      border-left: 3px solid #667eea;
      font-size: 0.9rem;
    }

    .preview-field strong {
      color: #2d3748;
      display: block;
      margin-bottom: 0.25rem;
    }

    .severity-badge {
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-weight: 600;
      font-size: 0.85rem;
      text-transform: uppercase;
    }

    .severity-critique, .severity-haute {
      background: #fed7d7;
      color: #c53030;
    }

    .severity-moyenne, .severity-moderee {
      background: #feebc8;
      color: #c05621;
    }

    .severity-faible, .severity-basse {
      background: #c6f6d5;
      color: #276749;
    }

    .result-content {
      margin: 1rem 0;
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease;
    }

    .result-content.expanded {
      max-height: 800px;
      overflow-y: auto;
    }

    .result-content pre {
      background: #2d3748;
      color: #e2e8f0;
      padding: 1rem;
      border-radius: 8px;
      overflow-x: auto;
      font-size: 0.85rem;
      line-height: 1.5;
      margin: 0;
    }

    .btn-toggle {
      padding: 0.5rem 1rem;
      background: #4299e1;
      color: white;
      border: none;
      border-radius: 6px;
      font-size: 0.85rem;
      cursor: pointer;
      transition: background 0.3s;
    }

    .btn-toggle:hover {
      background: #3182ce;
    }

    .no-results {
      text-align: center;
      padding: 3rem;
      color: #718096;
    }

    .no-results p {
      margin: 0.5rem 0;
      font-size: 1.1rem;
    }

    .hint {
      font-size: 0.9rem;
      color: #a0aec0;
    }

    /* Kibana iframe section */

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
  searchQuery: string = '';
  selectedIndex: string = '';
  resultsPerPage: number = 20;
  searchResults: SearchResult | null = null;
  isSearching: boolean = false;
  expandedResults: { [key: number]: boolean } = {};

  constructor(private searchService: ElasticsearchSearchService) {}

  ngOnInit() {
    console.log('Kibana Dashboard Component initialisé avec recherche Elasticsearch');
  }

  performSearch() {
    if (!this.searchQuery.trim() && !this.selectedIndex) {
      alert('Veuillez entrer une requête de recherche ou sélectionner un index');
      return;
    }

    this.isSearching = true;
    this.expandedResults = {};

    const searchRequest = {
      query: this.searchQuery.trim() || undefined,
      index: this.selectedIndex || undefined,
      size: this.resultsPerPage,
      sort_by: '@timestamp',
      sort_order: 'desc' as 'desc'
    };

    this.searchService.search(searchRequest).subscribe({
      next: (results) => {
        this.searchResults = results;
        this.isSearching = false;
        console.log('Résultats de recherche:', results);
      },
      error: (error) => {
        console.error('Erreur lors de la recherche:', error);
        this.searchResults = {
          total: 0,
          count: 0,
          documents: [],
          from: 0,
          size: this.resultsPerPage,
          error: error.message || 'Erreur lors de la recherche'
        };
        this.isSearching = false;
      }
    });
  }

  onIndexChange() {
    if (this.searchQuery || this.selectedIndex) {
      this.performSearch();
    }
  }

  clearSearch() {
    this.searchQuery = '';
    this.selectedIndex = '';
    this.searchResults = null;
    this.expandedResults = {};
  }

  toggleResult(index: number) {
    this.expandedResults[index] = !this.expandedResults[index];
  }
}
