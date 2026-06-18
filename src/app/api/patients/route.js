import connectDB from "@/lib/mongodb";
import Patient from "@/models/Patient";

export async function POST(req) {
  try {
    await connectDB();

    const body = await req.json();

    const patient = await Patient.create(body);

    return Response.json({
      success: true,
      data: patient,
    });
  } catch (error) {
    return Response.json(
      { success: false, error: error.message },
      { status: 500 }
    );
  }
}