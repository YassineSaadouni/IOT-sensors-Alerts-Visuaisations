import { Component, OnInit } from '@angular/core';
import { VehicleService } from '../../services/vehicle.service';
import { Vehicle, VehicleStatistics } from '../../models/models';

@Component({
  selector: 'app-vehicles',
  templateUrl: './vehicles.component.html',
  styleUrls: ['./vehicles.component.scss']
})
export class VehiclesComponent implements OnInit {
  vehicles: Vehicle[] = [];
  statistics: VehicleStatistics | null = null;
  loading = false;
  error: string | null = null;

  // Filters
  selectedStatus = '';
  selectedDriver = '';
  drivers: string[] = [];
  statuses = ['active', 'en_route', 'stopped', 'warning', 'critical'];

  // Pagination
  total = 0;
  page = 1;
  pageSize = 15;

  constructor(private vehicleService: VehicleService) {}

  ngOnInit(): void {
    this.loadVehicles();
    this.loadStatistics();
  }

  loadVehicles(): void {
    this.loading = true;
    this.error = null;

    const params: any = {
      size: this.pageSize,
      from: (this.page - 1) * this.pageSize
    };

    if (this.selectedStatus) {
      params.filters = { status: this.selectedStatus };
    }

    if (this.selectedDriver) {
      if (params.filters) {
        params.filters.driver = this.selectedDriver;
      } else {
        params.filters = { driver: this.selectedDriver };
      }
    }

    this.vehicleService.getVehicles(params).subscribe({
      next: (response) => {
        this.vehicles = response.documents;
        this.total = response.total;
        this.loading = false;

        // Extract unique drivers
        const driversSet = new Set<string>();
        response.documents.forEach(vehicle => {
          if (vehicle.driver) {
            driversSet.add(vehicle.driver);
          }
        });
        this.drivers = Array.from(driversSet).sort();
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement des véhicules';
        console.error('Error loading vehicles:', error);
        this.loading = false;
      }
    });
  }

  loadStatistics(): void {
    this.vehicleService.getStatistics().subscribe({
      next: (stats) => {
        this.statistics = stats;
      },
      error: (error) => {
        console.error('Error loading statistics:', error);
      }
    });
  }

  applyFilters(): void {
    this.page = 1;
    this.loadVehicles();
  }

  clearFilters(): void {
    this.selectedStatus = '';
    this.selectedDriver = '';
    this.page = 1;
    this.loadVehicles();
  }

  refresh(): void {
    this.loadVehicles();
    this.loadStatistics();
  }

  changePage(newPage: number): void {
    this.page = newPage;
    this.loadVehicles();
  }

  getStatusClass(status: string): string {
    const statusMap: { [key: string]: string } = {
      'active': 'badge-success',
      'en_route': 'badge-info',
      'stopped': 'badge-secondary',
      'warning': 'badge-warning',
      'critical': 'badge-danger'
    };
    return statusMap[status] || 'badge-secondary';
  }

  getSpeedClass(speed: number): string {
    if (speed > 100) return 'speed-high';
    if (speed > 50) return 'speed-medium';
    return 'speed-low';
  }

  getFuelClass(fuel: number): string {
    if (fuel > 60) return 'fuel-high';
    if (fuel > 30) return 'fuel-medium';
    return 'fuel-low';
  }

  getTotalPages(): number {
    return Math.ceil(this.total / this.pageSize);
  }

  getPageNumbers(): number[] {
    const totalPages = this.getTotalPages();
    const pages: number[] = [];
    const maxPages = 5;
    
    let startPage = Math.max(1, this.page - Math.floor(maxPages / 2));
    let endPage = Math.min(totalPages, startPage + maxPages - 1);
    
    if (endPage - startPage < maxPages - 1) {
      startPage = Math.max(1, endPage - maxPages + 1);
    }
    
    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }
    
    return pages;
  }
}
