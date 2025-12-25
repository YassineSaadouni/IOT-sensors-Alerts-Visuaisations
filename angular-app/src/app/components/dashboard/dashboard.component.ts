import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { ApiService } from '../../services/api.service';
import { FileUploadService } from '../../services/file-upload.service';
import { Statistics, HealthStatus } from '../../models/models';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {
  stats: Statistics | null = null;
  health: HealthStatus | null = null;
  loading = true;
  error: string | null = null;
  private uploadSubscription?: Subscription;

  constructor(
    private apiService: ApiService,
    private fileUploadService: FileUploadService
  ) {}

  ngOnInit(): void {
    this.loadData();
    
    // S'abonner aux événements d'upload pour rafraîchir automatiquement
    this.uploadSubscription = this.fileUploadService.uploadCompleted$.subscribe(() => {
      console.log('Upload détecté, rafraîchissement du dashboard...');
      setTimeout(() => this.loadData(), 1000);
    });
  }

  ngOnDestroy(): void {
    if (this.uploadSubscription) {
      this.uploadSubscription.unsubscribe();
    }
  }

  loadData(): void {
    this.loading = true;
    this.error = null;

    // Charger les statistiques
    this.apiService.getStatistics().subscribe({
      next: (data) => {
        this.stats = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Erreur lors du chargement des statistiques';
        this.loading = false;
        console.error(err);
      }
    });

    // Charger le health status
    this.apiService.getHealth().subscribe({
      next: (data) => {
        this.health = data;
      },
      error: (err) => {
        console.error('Erreur health check:', err);
      }
    });
  }

  refresh(): void {
    this.loadData();
  }

  getCountByFileType(fileType: string): number {
    if (!this.stats) return 0;
    const item = this.stats.by_file_type.find(f => f.key === fileType);
    return item ? item.count : 0;
  }

  getTimelineWidth(count: number): number {
    if (!this.stats || !this.stats.upload_timeline.length) return 0;
    const maxCount = Math.max(...this.stats.upload_timeline.map(t => t.count));
    return (count / maxCount) * 100;
  }
}
