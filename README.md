# BrainTumorAI Monorepo

Empowering healthcare professionals with state-of-the-art AI-powered MRI analysis for brain tumor detection, classification, and segmentation.

---

## 🏗️ Repository Architecture

The project has been organized into a clean monorepo structure to isolate the Next.js TypeScript web application and the Python Flask deep learning API.

```
/ (Root)
├── frontend/             # Next.js web application
│   ├── src/              # React frontend components & pages
│   ├── public/           # Static assets (icons, images)
│   ├── package.json      # Frontend package configuration
│   ├── tsconfig.json     # TypeScript configuration
│   └── ...
├── backend/              # Python Flask API
│   ├── app.py            # Flask API entry point
│   ├── predict.py        # ML prediction & Grad-CAM pipeline
│   ├── gradcam.py        # Grad-CAM heatmap generation
│   ├── segmentation.py   # OpenCV contour segmentation
│   ├── requirements.txt  # Python requirements
│   └── model/            # CNN Model weights (.keras)
├── scripts/              # Cross-platform orchestrator scripts (TS)
├── package.json          # Root scripts to run both apps & dev dependencies
├── tsconfig.json         # Workspace TypeScript configurations
└── README.md             # Monorepo setup guide
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) (App Router, React 19)
- **Language**: TypeScript (fully typed models & APIs)
- **Database**: MongoDB (via Mongoose)
- **Authentication**: Firebase Authentication
- **Icons**: Lucide React
- **Styling**: Tailwind CSS

### Backend
- **Framework**: Flask (with Flask-CORS)
- **Language**: Python 3.12+
- **Deep Learning**: TensorFlow / Keras (CNN model)
- **Computer Vision**: OpenCV (image processing & contour segmentation)
- **Visualization**: Matplotlib (Grad-CAM heatmaps)

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 📋 Prerequisites
- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)

---

### 1. Setup & Installation

First, run a quick install in the root directory to set up editor/VS Code types:
```bash
npm install
```

Then, install the dependencies for frontend and backend:

#### Frontend Setup
```bash
npm run install:frontend
```

#### Backend Setup
This creates a virtual environment and installs the required packages:
```bash
npm run install:backend
```

---

### 2. Configure Environment Variables

1. Go to the `frontend/` directory.
2. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```
3. Open `frontend/.env.local` and add your **Firebase Config** credentials and **MongoDB connection URI**.
4. The Python backend URL is pre-configured to `http://127.0.0.1:5000`.

---

### 3. Running the Application

You can start both servers from the root of the project using separate terminal windows.

#### Start the Next.js Frontend
```bash
npm run dev:frontend
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

#### Start the Python Flask Backend
```bash
npm run dev:backend
```
The API will run on [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🤖 AI Model Features
1. **Tumor Classification**: Classifies MRI scans into 4 types: `Glioma`, `Meningioma`, `Pituitary`, or `No Tumor`.
2. **Grad-CAM Visualizations**: Generates heatmaps indicating the visual features on which the CNN model focused its attention.
3. **Contour Segmentation**: Extracts and overlays contours to outline the shape, width, height, and surface area of the tumor.
4. **Severity Scoring**: Analyzes the calculated area of the segmented tumor to rate severity (`None`, `Low`, `Medium`, `High`, `Needs Review`).
