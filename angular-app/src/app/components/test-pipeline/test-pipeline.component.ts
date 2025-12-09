import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface AlerteTest {
  id_alerte: string;
  timestamp: string;
  type_alerte: string;
  categorie: string;
  severite: string;
  batiment: string;
  salle: string;
  zone: string;
  technicien_assigne: string;
  statut: string;
  description: string;
  temps_reponse_minutes?: number;
  resolution?: string;
}

@Component({
  selector: 'app-test-pipeline',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="test-pipeline-container">
      <div class="header">
        <h2>🧪 Test Pipeline IoT - Alertes</h2>
        <p>Envoyer des alertes test vers Redis → Logstash → Elasticsearch</p>
      </div>

      <!-- Formulaire de création d'alerte -->
      <div class="form-card">
        <h3>📝 Créer une nouvelle alerte</h3>
        
        <div class="form-grid">
          <div class="form-group">
            <label>Type d'alerte *</label>
            <select [(ngModel)]="nouvelleAlerte.type_alerte" required>
              <option value="">-- Sélectionner --</option>
              <option value="incendie">🔥 Incendie</option>
              <option value="intrusion">🚨 Intrusion</option>
              <option value="fuite">💧 Fuite d'eau</option>
              <option value="panne">⚡ Panne électrique</option>
              <option value="temperature">🌡️ Température anormale</option>
              <option value="securite">🔒 Sécurité</option>
            </select>
          </div>

          <div class="form-group">
            <label>Catégorie *</label>
            <select [(ngModel)]="nouvelleAlerte.categorie" required>
              <option value="">-- Sélectionner --</option>
              <option value="securite">🔒 Sécurité</option>
              <option value="technique">🔧 Technique</option>
              <option value="environnement">🌿 Environnement</option>
              <option value="energie">⚡ Énergie</option>
            </select>
          </div>

          <div class="form-group">
            <label>Sévérité *</label>
            <select [(ngModel)]="nouvelleAlerte.severite" required>
              <option value="">-- Sélectionner --</option>
              <option value="critique">🔴 Critique</option>
              <option value="haute">🟠 Haute</option>
              <option value="moyenne">🟡 Moyenne</option>
              <option value="faible">🟢 Faible</option>
            </select>
          </div>

          <div class="form-group">
            <label>Bâtiment *</label>
            <input type="text" [(ngModel)]="nouvelleAlerte.batiment" 
                   placeholder="Ex: Bâtiment A" required>
          </div>

          <div class="form-group">
            <label>Salle *</label>
            <input type="text" [(ngModel)]="nouvelleAlerte.salle" 
                   placeholder="Ex: Salle 101" required>
          </div>

          <div class="form-group">
            <label>Zone *</label>
            <input type="text" [(ngModel)]="nouvelleAlerte.zone" 
                   placeholder="Ex: Zone Nord" required>
          </div>

          <div class="form-group">
            <label>Technicien assigné</label>
            <input type="text" [(ngModel)]="nouvelleAlerte.technicien_assigne" 
                   placeholder="Ex: Jean Dupont">
          </div>

          <div class="form-group">
            <label>Statut</label>
            <select [(ngModel)]="nouvelleAlerte.statut">
              <option value="ouverte">🔓 Ouverte</option>
              <option value="en_cours">⏳ En cours</option>
              <option value="resolue">✅ Résolue</option>
              <option value="fermee">🔒 Fermée</option>
            </select>
          </div>

          <div class="form-group full-width">
            <label>Description *</label>
            <textarea [(ngModel)]="nouvelleAlerte.description" 
                      placeholder="Décrivez l'alerte en détail..." 
                      rows="3" required></textarea>
          </div>
        </div>

        <div class="form-actions">
          <button class="btn btn-primary" (click)="envoyerAlerte()" 
                  [disabled]="loading || !isFormValid()">
            <span *ngIf="!loading">📤 Envoyer l'alerte</span>
            <span *ngIf="loading">⏳ Envoi en cours...</span>
          </button>
          <button class="btn btn-secondary" (click)="genererAlertesTest()">
            🎲 Générer 5 alertes aléatoires
          </button>
          <button class="btn btn-reset" (click)="resetForm()">
            🔄 Réinitialiser
          </button>
        </div>
      </div>

      <!-- Messages de statut -->
      <div *ngIf="message" [class]="'message message-' + messageType">
        {{ message }}
      </div>

      <!-- Statistiques temps réel -->
      <div class="stats-card">
        <h3>📊 Statistiques de test</h3>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-value">{{ alertesEnvoyees }}</div>
            <div class="stat-label">Alertes envoyées</div>
          </div>
          <div class="stat-item success">
            <div class="stat-value">{{ alertesReussies }}</div>
            <div class="stat-label">Succès</div>
          </div>
          <div class="stat-item error">
            <div class="stat-value">{{ alertesEchouees }}</div>
            <div class="stat-label">Échecs</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ tempsReponseMs }}ms</div>
            <div class="stat-label">Temps réponse moyen</div>
          </div>
        </div>
      </div>

      <!-- Historique des envois -->
      <div class="history-card">
        <h3>📜 Historique des envois ({{ historique.length }} derniers)</h3>
        <div *ngIf="historique.length === 0" class="empty-state">
          Aucune alerte envoyée pour le moment
        </div>
        <div class="history-list">
          <div *ngFor="let item of historique" class="history-item" 
               [class.success]="item.success" [class.error]="!item.success">
            <div class="history-icon">
              {{ item.success ? '✅' : '❌' }}
            </div>
            <div class="history-content">
              <div class="history-title">
                {{ item.alerte.type_alerte }} - {{ item.alerte.severite }}
              </div>
              <div class="history-details">
                {{ item.alerte.batiment }} / {{ item.alerte.salle }} - {{ item.timestamp }}
              </div>
              <div class="history-message" *ngIf="item.message">
                {{ item.message }}
              </div>
            </div>
            <div class="history-time">
              {{ item.duree }}ms
            </div>
          </div>
        </div>
      </div>

      <!-- Guide d'utilisation -->
      <div class="guide-card">
        <h3>📖 Comment ça marche ?</h3>
        <ol>
          <li><strong>Remplissez le formulaire</strong> avec les détails de l'alerte</li>
          <li><strong>Cliquez sur "Envoyer l'alerte"</strong></li>
          <li>L'alerte est envoyée à l'<strong>API Django</strong> (port 8000)</li>
          <li>Django l'envoie vers <strong>Redis</strong></li>
          <li><strong>Logstash</strong> récupère de Redis et envoie à Elasticsearch</li>
          <li>L'alerte apparaît dans <strong>Kibana</strong> (dashboards)</li>
        </ol>
        <div class="pipeline-diagram">
          <span class="pipeline-step">Angular</span>
          <span class="pipeline-arrow">→</span>
          <span class="pipeline-step">Django API</span>
          <span class="pipeline-arrow">→</span>
          <span class="pipeline-step">Redis</span>
          <span class="pipeline-arrow">→</span>
          <span class="pipeline-step">Logstash</span>
          <span class="pipeline-arrow">→</span>
          <span class="pipeline-step">Elasticsearch</span>
          <span class="pipeline-arrow">→</span>
          <span class="pipeline-step">Kibana</span>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .test-pipeline-container {
      padding: 2rem;
      max-width: 1200px;
      margin: 0 auto;
    }

    .header {
      text-align: center;
      margin-bottom: 2rem;
    }

    .header h2 {
      color: #2d3748;
      margin-bottom: 0.5rem;
    }

    .header p {
      color: #718096;
    }

    .form-card, .stats-card, .history-card, .guide-card {
      background: white;
      padding: 1.5rem;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      margin-bottom: 1.5rem;
    }

    .form-card h3, .stats-card h3, .history-card h3, .guide-card h3 {
      margin-top: 0;
      margin-bottom: 1.5rem;
      color: #2d3748;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
    }

    .form-group.full-width {
      grid-column: 1 / -1;
    }

    .form-group label {
      margin-bottom: 0.5rem;
      font-weight: 600;
      color: #4a5568;
      font-size: 0.9rem;
    }

    .form-group input,
    .form-group select,
    .form-group textarea {
      padding: 0.75rem;
      border: 2px solid #e2e8f0;
      border-radius: 8px;
      font-size: 1rem;
      transition: border-color 0.3s;
    }

    .form-group input:focus,
    .form-group select:focus,
    .form-group textarea:focus {
      outline: none;
      border-color: #667eea;
    }

    .form-actions {
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
    }

    .btn {
      padding: 0.75rem 1.5rem;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s;
    }

    .btn-primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }

    .btn-primary:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    .btn-primary:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .btn-secondary {
      background: #48bb78;
      color: white;
    }

    .btn-secondary:hover {
      background: #38a169;
      transform: translateY(-2px);
    }

    .btn-reset {
      background: #718096;
      color: white;
    }

    .btn-reset:hover {
      background: #4a5568;
    }

    .message {
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 1.5rem;
      font-weight: 500;
    }

    .message-success {
      background: #c6f6d5;
      color: #22543d;
      border-left: 4px solid #48bb78;
    }

    .message-error {
      background: #fed7d7;
      color: #742a2a;
      border-left: 4px solid #f56565;
    }

    .message-info {
      background: #bee3f8;
      color: #2c5282;
      border-left: 4px solid #4299e1;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 1rem;
    }

    .stat-item {
      text-align: center;
      padding: 1rem;
      background: #f7fafc;
      border-radius: 8px;
      border: 2px solid #e2e8f0;
    }

    .stat-item.success {
      background: #c6f6d5;
      border-color: #48bb78;
    }

    .stat-item.error {
      background: #fed7d7;
      border-color: #f56565;
    }

    .stat-value {
      font-size: 2rem;
      font-weight: 700;
      color: #2d3748;
    }

    .stat-label {
      font-size: 0.85rem;
      color: #718096;
      margin-top: 0.25rem;
    }

    .empty-state {
      text-align: center;
      padding: 2rem;
      color: #a0aec0;
      font-style: italic;
    }

    .history-list {
      max-height: 400px;
      overflow-y: auto;
    }

    .history-item {
      display: flex;
      align-items: center;
      padding: 1rem;
      border: 2px solid #e2e8f0;
      border-radius: 8px;
      margin-bottom: 0.75rem;
      transition: all 0.3s;
    }

    .history-item:hover {
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .history-item.success {
      border-left: 4px solid #48bb78;
    }

    .history-item.error {
      border-left: 4px solid #f56565;
    }

    .history-icon {
      font-size: 1.5rem;
      margin-right: 1rem;
    }

    .history-content {
      flex: 1;
    }

    .history-title {
      font-weight: 600;
      color: #2d3748;
      margin-bottom: 0.25rem;
    }

    .history-details {
      font-size: 0.85rem;
      color: #718096;
    }

    .history-message {
      font-size: 0.8rem;
      color: #a0aec0;
      margin-top: 0.25rem;
    }

    .history-time {
      font-weight: 600;
      color: #667eea;
    }

    .guide-card ol {
      margin: 1rem 0;
      padding-left: 1.5rem;
    }

    .guide-card li {
      margin-bottom: 0.75rem;
      color: #4a5568;
      line-height: 1.6;
    }

    .pipeline-diagram {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1.5rem;
      padding: 1rem;
      background: #f7fafc;
      border-radius: 8px;
    }

    .pipeline-step {
      padding: 0.5rem 1rem;
      background: white;
      border: 2px solid #667eea;
      border-radius: 6px;
      font-weight: 600;
      color: #667eea;
      font-size: 0.9rem;
    }

    .pipeline-arrow {
      font-size: 1.5rem;
      color: #667eea;
    }

    @media (max-width: 768px) {
      .form-grid {
        grid-template-columns: 1fr;
      }

      .form-actions {
        flex-direction: column;
      }

      .btn {
        width: 100%;
      }

      .pipeline-diagram {
        flex-direction: column;
      }

      .pipeline-arrow {
        transform: rotate(90deg);
      }
    }
  `]
})
export class TestPipelineComponent implements OnInit {
  apiUrl = 'http://localhost:8000/api';
  loading = false;
  message = '';
  messageType: 'success' | 'error' | 'info' = 'info';

  // Statistiques
  alertesEnvoyees = 0;
  alertesReussies = 0;
  alertesEchouees = 0;
  tempsReponseMs = 0;
  tempsTotal = 0;

  // Historique
  historique: any[] = [];

  // Formulaire
  nouvelleAlerte: AlerteTest = {
    id_alerte: '',
    timestamp: '',
    type_alerte: '',
    categorie: '',
    severite: '',
    batiment: '',
    salle: '',
    zone: '',
    technicien_assigne: '',
    statut: 'ouverte',
    description: ''
  };

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.resetForm();
  }

  resetForm() {
    this.nouvelleAlerte = {
      id_alerte: this.genererIdAlerte(),
      timestamp: new Date().toISOString(),
      type_alerte: '',
      categorie: '',
      severite: '',
      batiment: 'Bâtiment A',
      salle: 'Salle 101',
      zone: 'Zone Nord',
      technicien_assigne: '',
      statut: 'ouverte',
      description: ''
    };
  }

  genererIdAlerte(): string {
    return 'ALT-TEST-' + Date.now() + '-' + Math.random().toString(36).substr(2, 5).toUpperCase();
  }

  isFormValid(): boolean {
    return !!(
      this.nouvelleAlerte.type_alerte &&
      this.nouvelleAlerte.categorie &&
      this.nouvelleAlerte.severite &&
      this.nouvelleAlerte.batiment &&
      this.nouvelleAlerte.salle &&
      this.nouvelleAlerte.zone &&
      this.nouvelleAlerte.description
    );
  }

  async envoyerAlerte() {
    if (!this.isFormValid()) {
      this.showMessage('Veuillez remplir tous les champs obligatoires', 'error');
      return;
    }

    this.loading = true;
    this.message = '';
    const startTime = Date.now();

    // Mise à jour timestamp
    this.nouvelleAlerte.timestamp = new Date().toISOString();

    try {
      const response = await this.http.post(
        `${this.apiUrl}/alertes/`,
        this.nouvelleAlerte
      ).toPromise();

      const duree = Date.now() - startTime;
      
      this.alertesEnvoyees++;
      this.alertesReussies++;
      this.tempsTotal += duree;
      this.tempsReponseMs = Math.round(this.tempsTotal / this.alertesEnvoyees);

      this.historique.unshift({
        alerte: { ...this.nouvelleAlerte },
        success: true,
        timestamp: new Date().toLocaleString('fr-FR'),
        duree: duree,
        message: 'Envoyée avec succès vers le pipeline'
      });

      if (this.historique.length > 10) {
        this.historique.pop();
      }

      this.showMessage(
        `✅ Alerte envoyée avec succès! (${duree}ms)\n` +
        `Pipeline: Angular → Django → Redis → Logstash → Elasticsearch → Kibana`,
        'success'
      );

      // Réinitialiser le formulaire avec un nouvel ID
      setTimeout(() => {
        this.resetForm();
      }, 2000);

    } catch (error: any) {
      const duree = Date.now() - startTime;
      
      this.alertesEnvoyees++;
      this.alertesEchouees++;

      this.historique.unshift({
        alerte: { ...this.nouvelleAlerte },
        success: false,
        timestamp: new Date().toLocaleString('fr-FR'),
        duree: duree,
        message: error.message || 'Erreur inconnue'
      });

      if (this.historique.length > 10) {
        this.historique.pop();
      }

      this.showMessage(
        `❌ Erreur lors de l'envoi: ${error.message || 'Vérifiez que Django est démarré'}`,
        'error'
      );
    } finally {
      this.loading = false;
    }
  }

  async genererAlertesTest() {
    const types = ['incendie', 'intrusion', 'fuite', 'panne', 'temperature', 'securite'];
    const categories = ['securite', 'technique', 'environnement', 'energie'];
    const severites = ['critique', 'haute', 'moyenne', 'faible'];
    const batiments = ['Bâtiment A', 'Bâtiment B', 'Bâtiment C'];
    const salles = ['Salle 101', 'Salle 102', 'Salle 201', 'Salle 202'];
    const zones = ['Zone Nord', 'Zone Sud', 'Zone Est', 'Zone Ouest'];
    const techniciens = ['Jean Dupont', 'Marie Martin', 'Pierre Dubois', ''];

    this.showMessage('🎲 Génération de 5 alertes aléatoires...', 'info');

    for (let i = 0; i < 5; i++) {
      this.nouvelleAlerte = {
        id_alerte: this.genererIdAlerte(),
        timestamp: new Date().toISOString(),
        type_alerte: types[Math.floor(Math.random() * types.length)],
        categorie: categories[Math.floor(Math.random() * categories.length)],
        severite: severites[Math.floor(Math.random() * severites.length)],
        batiment: batiments[Math.floor(Math.random() * batiments.length)],
        salle: salles[Math.floor(Math.random() * salles.length)],
        zone: zones[Math.floor(Math.random() * zones.length)],
        technicien_assigne: techniciens[Math.floor(Math.random() * techniciens.length)],
        statut: 'ouverte',
        description: `Alerte test générée automatiquement - ${new Date().toLocaleString('fr-FR')}`
      };

      await this.envoyerAlerte();
      await this.delay(500); // Pause 500ms entre chaque envoi
    }

    this.showMessage('✅ 5 alertes générées et envoyées!', 'success');
  }

  showMessage(msg: string, type: 'success' | 'error' | 'info') {
    this.message = msg;
    this.messageType = type;
    setTimeout(() => {
      this.message = '';
    }, 5000);
  }

  delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
