import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-kibana-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="dashboard-container">
      <div class="dashboard-header">
        <h2>{{ title }}</h2>
        
        <div class="dashboard-selector">
          <button (click)="loadDashboard('overview')" 
                  [class.active]="currentDashboard === 'overview'">
            🏠 Vue d'ensemble
          </button>
          <button (click)="loadDashboard('alertes')" 
                  [class.active]="currentDashboard === 'alertes'">
            🚨 Alertes
          </button>
          <button (click)="loadDashboard('capteurs')" 
                  [class.active]="currentDashboard === 'capteurs'">
            🌡️ Capteurs
          </button>
          <button (click)="loadDashboard('consommation')" 
                  [class.active]="currentDashboard === 'consommation'">
            ⚡ Consommation
          </button>
          <button (click)="loadDashboard('occupation')" 
                  [class.active]="currentDashboard === 'occupation'">
            🏢 Occupation
          </button>
          <button (click)="loadDashboard('maintenance')" 
                  [class.active]="currentDashboard === 'maintenance'">
            🔧 Maintenance
          </button>
        </div>
        
        <div class="dashboard-actions">
          <button (click)="refreshDashboard()" class="btn-refresh">
            🔄 Actualiser
          </button>
          <a [href]="kibanaUrl + '/app/dashboards#/view/' + dashboards[currentDashboard]" 
             target="_blank" 
             class="btn-external">
            🔗 Ouvrir dans Kibana
          </a>
        </div>
      </div>
      
      <div class="dashboard-content">
        <iframe 
          *ngIf="dashboardUrl"
          [src]="dashboardUrl" 
          class="kibana-iframe"
          frameborder="0"
          (load)="onLoad()">
        </iframe>
        
        <div *ngIf="loading" class="loading-overlay">
          <div class="spinner"></div>
          <p>Chargement du dashboard...</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      height: 100%;
      display: flex;
      flex-direction: column;
    }
    
    .dashboard-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      background: #f5f5f5;
      border-bottom: 2px solid #ddd;
    }
    
    .dashboard-header h2 {
      margin: 0;
      color: #333;
    }
    
    .dashboard-actions {
      display: flex;
      gap: 0.5rem;
    }
    
    .btn-refresh, .btn-external {
      padding: 0.5rem 1rem;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      text-decoration: none;
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
  title: string = 'Dashboard IoT';
  kibanaUrl: string = 'http://localhost:5601';
  
  // IDs des dashboards Kibana (recuperes automatiquement)
  dashboards: { [key: string]: string } = {
    alertes: 'dashboard-alertes',
    capteurs: 'dashboard-capteurs',
    consommation: 'dashboard-consommation',
    occupation: 'dashboard-occupation',
    maintenance: 'dashboard-maintenance',
    overview: 'dashboard-overview'
  };
  
  currentDashboard: string = 'alertes';
  dashboardUrl: SafeResourceUrl | null = null;
  loading: boolean = true;
  
  constructor(private sanitizer: DomSanitizer) {}
  
  ngOnInit() {
    this.loadDashboard();
  }
  
  loadDashboard(type?: string) {
    if (type) {
      this.currentDashboard = type;
    }
    
    this.loading = true;
    const dashboardId = this.dashboards[this.currentDashboard as keyof typeof this.dashboards];
    
    // URL avec embed=true pour integration iframe
    const url = `${this.kibanaUrl}/app/dashboards#/view/${dashboardId}?embed=true&_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-30d,to:now))&_a=(description:'',filters:!(),fullScreenMode:!f,options:(hidePanelTitles:!f,useMargins:!t),query:(language:kuery,query:''),timeRestore:!f,title:'',viewMode:view)`;
    this.dashboardUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
  
  refreshDashboard() {
    const currentUrl = this.dashboardUrl;
    this.dashboardUrl = null;
    setTimeout(() => {
      this.dashboardUrl = currentUrl;
    }, 100);
  }
  
  onLoad() {
    this.loading = false;
  }
}
