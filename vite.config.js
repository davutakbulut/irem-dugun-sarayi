import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['react', 'react-dom'],
          'page-create-reservation': ['./src/pages/CreateReservationPage.jsx'],
          'page-reservations-list': ['./src/pages/ReservationsListPage.jsx'],
          'page-dashboard': ['./src/pages/DashboardPage.jsx'],
          'page-calendar': ['./src/pages/CalendarPage.jsx'],
          'page-finance': ['./src/pages/FinancePage.jsx'],
          'page-customers': ['./src/pages/CustomersPage.jsx'],
          'page-media': ['./src/pages/MediaPage.jsx'],
          'page-settings': ['./src/pages/SettingsPage.jsx']
        }
      }
    }
  },
  server: {
    port: 8000,
    host: true
  }
});
