import { Component } from '@angular/core';

@Component({
  selector: 'app-navbar',
  template: `
    <nav class="navbar">
      <div class="nav-brand">
        <h2>🌐 IoT Dashboard</h2>
      </div>
      <ul class="nav-menu">
        <li><a routerLink="/kibana" routerLinkActive="active">📈 Kibana Dashboards</a></li>
        <li><a routerLink="/dashboard" routerLinkActive="active">📊 Dashboard</a></li>
        <li><a routerLink="/upload" routerLinkActive="active">📤 Upload</a></li>
      </ul>
    </nav>
  `,
  styles: [`
    .navbar {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .nav-brand h2 {
      margin: 0;
      font-size: 1.5rem;
    }

    .nav-menu {
      display: flex;
      list-style: none;
      gap: 2rem;
      margin: 0;
    }

    .nav-menu a {
      color: white;
      text-decoration: none;
      padding: 0.5rem 1rem;
      border-radius: 5px;
      transition: background 0.3s ease;
    }

    .nav-menu a:hover, .nav-menu a.active {
      background: rgba(255, 255, 255, 0.2);
    }
  `]
})
export class NavbarComponent {}
