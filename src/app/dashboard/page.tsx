// "use client";

// import { signOut } from "firebase/auth";
// // import { auth } from "../firebase";
// import { auth } from "../../firebase";
// import { useRouter } from "next/navigation";

// export default function DashboardPage() {
//   const router = useRouter();

//   const handleLogout = async () => {
//     try {
//       await signOut(auth);
//       router.push("/login");
//     } catch (error) {
//       console.log(error);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-slate-950 text-white">
//       {/* Navbar */}
//       <nav className="flex justify-between items-center px-8 py-5 border-b border-slate-800">
//         <h1 className="text-3xl font-bold text-blue-500">
//           BrainTumorAI
//         </h1>

//         <button
//           onClick={handleLogout}
//           className="bg-red-600 hover:bg-red-700 px-5 py-2 rounded-xl"
//         >
//           Logout
//         </button>
//       </nav>

//       {/* Main Content */}
//       <div className="max-w-6xl mx-auto p-8">
//         <h2 className="text-4xl font-bold mb-2">
//           Welcome, Doctor 👨‍⚕️
//         </h2>

//         <p className="text-slate-400 mb-10">
//           Upload MRI scans and detect brain tumors with AI assistance.
//         </p>

//         {/* Cards */}
//         <div className="grid md:grid-cols-3 gap-8">
//           {/* Upload MRI */}
//           <div className="bg-slate-900 rounded-3xl p-8 shadow-xl">
//             <h3 className="text-2xl font-semibold mb-4">
//               🧠 Upload MRI Scan
//             </h3>

//             <p className="text-slate-400 mb-6">
//               Upload patient MRI images for analysis.
//             </p>

//             <button className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-xl">
//               Upload Image
//             </button>
//           </div>

//           {/* Prediction */}
//           <div className="bg-slate-900 rounded-3xl p-8 shadow-xl">
//             <h3 className="text-2xl font-semibold mb-4">
//               📊 Prediction Result
//             </h3>

//             <p className="text-slate-400 mb-6">
//               View AI-generated tumor classification.
//             </p>

//             <button className="w-full bg-green-600 hover:bg-green-700 py-3 rounded-xl">
//               View Result
//             </button>
//           </div>

//           {/* Patient History */}
//           <div className="bg-slate-900 rounded-3xl p-8 shadow-xl">
//             <h3 className="text-2xl font-semibold mb-4">
//               📜 Patient Records
//             </h3>

//             <p className="text-slate-400 mb-6">
//               Access previous diagnosis history.
//             </p>

//             <button className="w-full bg-purple-600 hover:bg-purple-700 py-3 rounded-xl">
//               View Records
//             </button>
//           </div>
//         </div>

//         {/* Recent Activity */}
//         <div className="mt-12 bg-slate-900 rounded-3xl p-8 shadow-xl">
//           <h2 className="text-3xl font-bold mb-6">
//             Recent Activity
//           </h2>

//           <div className="space-y-4">
//             <div className="bg-slate-800 p-4 rounded-xl">
//               Patient ID: #1023 — MRI Uploaded
//             </div>

//             <div className="bg-slate-800 p-4 rounded-xl">
//               Patient ID: #1018 — Prediction Completed
//             </div>

//             <div className="bg-slate-800 p-4 rounded-xl">
//               Patient ID: #1009 — Records Viewed
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }
"use client";

import { signOut } from "firebase/auth";
import { auth } from "../../firebase";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function DashboardPage() {
  const router = useRouter();

  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);

  const handleLogout = async () => {
    await signOut(auth);
    router.push("/login");
  };

  // 🔥 Fetch patients from MongoDB
  const fetchPatients = async () => {
    try {
      const user = auth.currentUser;

      const res = await fetch("/api/patients?doctorId=" + user.uid);
      const data = await res.json();

      setPatients(data.data || []);
      setLoading(false);
    } catch (err) {
      console.log(err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Navbar */}
      <nav className="flex justify-between items-center px-8 py-5 border-b border-slate-800">
        <h1 className="text-3xl font-bold text-blue-500">
          BrainTumorAI
        </h1>

        <button
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700 px-5 py-2 rounded-xl"
        >
          Logout
        </button>
      </nav>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto p-8">
        <h2 className="text-4xl font-bold mb-2">
          Welcome, Doctor 👨‍⚕️
        </h2>

        <p className="text-slate-400 mb-10">
          Upload MRI scans and detect brain tumors with AI assistance.
        </p>

        {/* Cards */}
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-slate-900 rounded-3xl p-8 shadow-xl">
            <h3 className="text-2xl font-semibold mb-4">
              🧠 Upload MRI Scan
            </h3>
            <p className="text-slate-400 mb-6">
              Upload patient MRI images for analysis.
            </p>
            <button className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-xl">
              Upload Image
            </button>
          </div>

          <div className="bg-slate-900 rounded-3xl p-8 shadow-xl">
            <h3 className="text-2xl font-semibold mb-4">
              📊 Prediction Result
            </h3>
            <p className="text-slate-400 mb-6">
              View AI-generated tumor classification.
            </p>
            <button className="w-full bg-green-600 hover:bg-green-700 py-3 rounded-xl">
              View Result
            </button>
          </div>

          <div className="bg-slate-900 rounded-3xl p-8 shadow-xl">
            <h3 className="text-2xl font-semibold mb-4">
              📜 Patient Records
            </h3>
            <p className="text-slate-400 mb-6">
              Access previous diagnosis history.
            </p>
            <button className="w-full bg-purple-600 hover:bg-purple-700 py-3 rounded-xl">
              View Records
            </button>
          </div>
        </div>

        {/* 🧠 REAL PATIENT RECORDS SECTION */}
        <div className="mt-12 bg-slate-900 rounded-3xl p-8 shadow-xl">
          <h2 className="text-3xl font-bold mb-6">
            Patient Records
          </h2>

          {loading ? (
            <p className="text-slate-400">Loading records...</p>
          ) : patients.length === 0 ? (
            <p className="text-slate-400">No patient records found.</p>
          ) : (
            <div className="space-y-4">
              {patients.map((p) => (
                <div
                  key={p._id}
                  className="bg-slate-800 p-4 rounded-xl"
                >
                  <p><b>Name:</b> {p.patientName}</p>
                  <p><b>Age:</b> {p.patientAge}</p>
                  <p><b>Type:</b> {p.tumorType}</p>
                  <p><b>Confidence:</b> {p.confidence}%</p>
                  <p><b>Status:</b> {p.status}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}