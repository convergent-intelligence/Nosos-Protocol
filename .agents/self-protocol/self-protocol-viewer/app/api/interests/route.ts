import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  const interestsPath = path.join(process.cwd(), '../Interests/tracked/interests.log');
  try {
    const interestsLog = fs.readFileSync(interestsPath, 'utf8');
    const interests = interestsLog.split('\n').filter(line => line.trim() !== '');
    return NextResponse.json({ interests });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to read interests log.' }, { status: 500 });
  }
}
