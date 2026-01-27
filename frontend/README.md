# Demmonstrator for tutorial

This is a simple full-stack application the frontend for the application, built with Vue 3 and Bootstrap 5, using Vite
as the build tool. The application provides a user interface for managing veterinary/pathology cases, including features
for listing, adding, and deleting cases, as well as managing breeds and sexes.

## Features

- Responsive, Bootstrap-styled UI
- Table-based case management with add/delete functionality
- Dynamic dropdowns for breed and sex selection
- Vertical and horizontal alignment improvements for table content
- Proxy setup for API requests to a backend server

## Project Structure

```asciiart
frontend/                 # Frontend root: Vue 3 app, config, and static assets
├── index.html            # Main HTML entry point for the SPA
├── package.json          # NPM dependencies and scripts
├── vite.config.js        # Vite build and dev server configuration
├── public/               # Static public assets
│   ├── css/
│   │   └── base.css      # Custom base CSS overrides
│   └── logos_icons/
│       └── ...           # Logo and icon image assets
├── src/                  # Application source code
│   ├── App.vue           # Main Vue app component
│   ├── main.js           # JS entry point, mounts Vue app
│   └── components/
│       ├── CaseList.vue  # Case list/table component
│       └── Layout.vue    # Layout and navigation component
```

## Prerequisites

- Node.js (v16 or later recommended)
- npm (v8 or later recommended)

## Installation

1. Navigate to the `frontend` directory:

   ```sh
   cd new_app/frontend
   ```

2. Install dependencies:

   ```sh
   npm install
   ```

## Running in Development Mode

Start the Vite development server:

```sh
npm run dev
```

- The app will be available at `http://localhost:5173` by default.
- API requests to `/api` are proxied to `http://localhost:8000` (see `vite.config.js`).

## Building for Production

To build the app for production:

```sh
npm run build
```

- The production-ready files will be output to the `../dist` directory (relative to `frontend`).

## Previewing the Production Build

To preview the production build locally:

```sh
npm run serve
```

- This will serve the built files at `http://localhost:4173` by default.

## Customization

- **Bootstrap**: The project uses Bootstrap 5 for styling. You can customize styles in `public/css/base.css` or override
  Bootstrap classes as needed.
- **API Proxy**: The Vite dev server proxies `/api` requests to the backend. Adjust the proxy target in `vite.config.js`
  if your backend runs elsewhere.

## Notes

- The frontend expects a compatible backend API for cases, breeds, and sexes at `/api/case`, `/api/breed`, and
  `/api/sex`.
- Deployment banner and branding can be customized via props in `App.vue` and `Layout.vue`.

## License

This project is private and not licensed for redistribution.
