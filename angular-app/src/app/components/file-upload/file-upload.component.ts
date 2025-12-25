import { Component, OnInit } from '@angular/core';
import { FileUploadService } from '../../services/file-upload.service';
import { FileUploadHistory } from '../../models/models';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss']
})
export class FileUploadComponent implements OnInit {
  selectedFile: File | null = null;
  selectedDataType: string = 'auto'; // Type de données: alertes, capteurs, etc.
  uploading = false;
  uploadProgress = 0;
  uploadSuccess = false;
  uploadError: string | null = null;
  uploadResponse: any = null;
  isDragging = false;

  // Types de données disponibles
  dataTypes = [
    { value: 'auto', label: '🤖 Détection automatique' },
    { value: 'alertes', label: '🚨 Alertes' },
    { value: 'capteurs', label: '📡 Capteurs' },
    { value: 'consommation', label: '⚡ Consommation' },
    { value: 'occupation', label: '👥 Occupation' },
    { value: 'maintenance', label: '🔧 Maintenance' }
  ];

  // Upload history
  history: FileUploadHistory[] = [];
  loadingHistory = false;

  // Statistics
  stats: any = {
    total_uploads: 0,
    by_file_type: [],
    by_data_type: []
  };

  constructor(private fileUploadService: FileUploadService) {}

  ngOnInit(): void {
    this.loadHistory();
    this.loadStats();
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.handleFile(files[0]);
    }
  }

  onFileSelected(event: any): void {
    const file = event.target.files?.[0];
    if (file) {
      this.handleFile(file);
    }
  }

  handleFile(file: File): void {
    // Validate file type
    const validTypes = ['text/csv', 'application/json', 'text/json'];
    const isCSV = file.name.endsWith('.csv');
    const isJSON = file.name.endsWith('.json');

    if (!isCSV && !isJSON && !validTypes.includes(file.type)) {
      this.uploadError = 'Format de fichier non valide. Seuls les fichiers CSV et JSON sont acceptés.';
      return;
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      this.uploadError = 'Le fichier est trop volumineux. Taille maximale: 10MB';
      return;
    }

    this.selectedFile = file;
    this.uploadError = null;
    this.uploadSuccess = false;
  }

  uploadFile(): void {
    if (!this.selectedFile) {
      this.uploadError = 'Veuillez sélectionner un fichier';
      return;
    }

    this.uploading = true;
    this.uploadProgress = 0;
    this.uploadError = null;
    this.uploadSuccess = false;
    this.uploadResponse = null;

    // Simulate progress (since the API doesn't support progress events)
    const progressInterval = setInterval(() => {
      if (this.uploadProgress < 90) {
        this.uploadProgress += 10;
      }
    }, 200);

    // Préparer le FormData avec le type de données
    const formData = new FormData();
    formData.append('file', this.selectedFile);
    
    // Ajouter data_type seulement si ce n'est pas 'auto'
    if (this.selectedDataType && this.selectedDataType !== 'auto') {
      formData.append('data_type', this.selectedDataType);
    }

    this.fileUploadService.uploadFileWithType(formData).subscribe({
      next: (response) => {
        clearInterval(progressInterval);
        this.uploadProgress = 100;
        this.uploading = false;
        this.uploadSuccess = true;
        this.uploadResponse = response;
        
        console.log('Upload successful:', response);

        // Reload history and stats
        setTimeout(() => {
          this.loadHistory();
          this.loadStats();
        }, 500);

        // Reset success message after 5 seconds
        setTimeout(() => {
          this.uploadSuccess = false;
          this.uploadResponse = null;
          this.selectedFile = null;
        }, 5000);
      },
      error: (error) => {
        clearInterval(progressInterval);
        this.uploading = false;
        this.uploadProgress = 0;
        this.uploadError = error.error?.message || 'Erreur lors de l\'upload du fichier';
        console.error('Upload error:', error);
      }
    });
  }

  loadHistory(): void {
    this.loadingHistory = true;
    this.fileUploadService.getRecentUploads().subscribe({
      next: (response) => {
        this.history = response?.uploads || [];
        this.loadingHistory = false;
      },
      error: (error) => {
        console.error('Error loading history:', error);
        this.history = [];
        this.loadingHistory = false;
      }
    });
  }

  loadStats(): void {
    this.fileUploadService.getUploadStats().subscribe({
      next: (stats) => {
        this.stats = stats || { total_uploads: 0, by_file_type: [], by_data_type: [] };
      },
      error: (error) => {
        console.error('Error loading stats:', error);
        this.stats = { total_uploads: 0, by_file_type: [], by_data_type: [] };
      }
    });
  }

  removeFile(): void {
    this.selectedFile = null;
    this.uploadError = null;
    this.uploadSuccess = false;
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }

  getFileIcon(filename: string): string {
    if (filename.endsWith('.csv')) return '📊';
    if (filename.endsWith('.json')) return '📄';
    return '📁';
  }

  getStatusClass(status: string): string {
    const statusMap: { [key: string]: string } = {
      'success': 'badge-success',
      'pending': 'badge-warning',
      'error': 'badge-danger',
      'processing': 'badge-info'
    };
    return statusMap[status] || 'badge-secondary';
  }
}
