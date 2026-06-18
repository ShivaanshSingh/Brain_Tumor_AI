import mongoose from "mongoose";

const patientSchema = new mongoose.Schema(
  {
    doctorId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Doctor",
      required: true,
    },

    patientName: {
      type: String,
      required: true,
    },

    patientAge: {
      type: Number,
      required: true,
    },

    patientGender: {
      type: String,
      enum: ["Male", "Female", "Other"],
      required: true,
    },

    imagePath: {
      type: String,
      required: true,
    },

    heatmapPath: String,

    tumorType: {
      type: String,
      enum: ["Glioma", "Meningioma", "Pituitary", "No Tumor"],
    },

    confidence: Number,

    probabilities: {
      glioma: Number,
      meningioma: Number,
      pituitary: Number,
      noTumor: Number,
    },

    notes: String,

    reportPdf: String,

    status: {
      type: String,
      enum: ["Processing", "Completed", "Failed"],
      default: "Processing",
    },

    scanDate: {
      type: Date,
      default: Date.now,
    },
  },
  {
    timestamps: true,
  }
);

export default mongoose.models.Patient ||
  mongoose.model("Patient", patientSchema);