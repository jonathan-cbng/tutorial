# Demonstration frontend for tutorial

> **Note**: For overall project information, see the [main README](../README.md).

This is the frontend for a simple full-stack application, built with Vue 3 and Bootstrap 5, using Vite as the build
tool. The application provides a user interface for managing veterinary and pathology cases, including features for
listing, adding, and deleting cases, as well as managing breeds and sexes.

## Features

- Responsive, Bootstrap-styled UI
- Table-based case management with add/delete functionality
- Dynamic dropdowns for breed and sex selection
- Vertical and horizontal alignment improvements for table content
- Proxy setup for API requests to a backend server

## Project Structure

```asciiart
frontend/                    # Frontend root: Vue 3 app, config, and static assets
├── index.html               # Main HTML entry point for the SPA
├── package.json             # NPM dependencies and scripts
├── vite.config.js           # Vite build and dev server configuration
├── Makefile                 # Build and deployment tasks
├── public/                  # Static public assets
│   ├── css/
│   │   └── base.css         # Custom base CSS overrides
│   └── logos_icons/         # Logo and icon image assets
├── src/                     # Application source code
│   ├── App.vue              # Main Vue app component
│   ├── main.js              # JS entry point, mounts Vue app
│   ├── router.js            # Vue Router configuration
│   ├── api.js               # API client for backend requests
│   ├── dompurify.js         # DOM purification utility
│   └── components/
│       ├── CaseList.vue     # Case list/table component
│       ├── CaseListView.vue # Case list view wrapper
│       ├── CaseCreate.vue   # Create new case form
│       ├── CaseEdit.vue     # Edit case form
│       ├── CaseDetails.vue  # Case details display
│       ├── CaseInfo.vue     # Case information component
│       ├── CaseSearchBox.vue # Case search functionality
│       └── Layout.vue       # Layout and navigation component
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

- The production-ready files will be output to the `dist` directory, which can then be served directly from the FastAPI
  backend server.

## Previewing the Production Build

To preview the production build locally:

```sh
npm run serve
```

- This will serve the built files at `http://localhost:4173` by default.

## Customisation

- **Bootstrap**: The project uses Bootstrap 5 for styling. You can customise styles in `public/css/base.css` or override
  Bootstrap classes as needed.
- **API Proxy**: The Vite dev server proxies `/api` requests to the backend. Adjust the proxy target in `vite.config.js`
  if your backend runs elsewhere.

## Notes

- The frontend expects a compatible backend API for cases, breeds, and sexes at `/api/case`, `/api/breed`, and
  `/api/sex`.
- Deployment banner and branding can be customised via props in `App.vue` and `Layout.vue`.

## License

This project is private and not licensed for redistribution.
