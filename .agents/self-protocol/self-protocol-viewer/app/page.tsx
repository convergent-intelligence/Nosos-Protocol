"use client";

import { useEffect, useState } from 'react';

export default function Home() {
  const [interests, setInterests] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchInterests() {
      try {
        const response = await fetch('/api/interests');
        if (!response.ok) {
          throw new Error('Failed to fetch interests');
        }
        const data = await response.json();
        setInterests(data.interests);
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError('An unknown error occurred');
        }
      }
    }

    fetchInterests();
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center py-32 px-16 bg-white dark:bg-black sm:items-start">
        <h1 className="text-3xl font-semibold leading-10 tracking-tight text-black dark:text-zinc-50">
          Self-Protocol Viewer
        </h1>
        <div className="mt-8">
          <h2 className="text-2xl font-semibold text-black dark:text-zinc-50">Interests</h2>
          {error && <p className="text-red-500">{error}</p>}
          <ul>
            {interests.map((interest, index) => (
              <li key={index} className="text-zinc-600 dark:text-zinc-400">{interest}</li>
            ))}
          </ul>
        </div>
      </main>
    </div>
  );
}
