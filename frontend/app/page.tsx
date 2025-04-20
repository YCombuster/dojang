'use client';

import { useState } from 'react';
import FileUpload from '@/components/FileUpload';
import UrlInput from '@/components/UrlInput';

export default function Home() {
    const [isLoading, setIsLoading] = useState(false);

    const handleFileSelect = async (file: File) => {
        try {
            setIsLoading(true);
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const data = await response.json();
            // Handle the response data here
            console.log(data);
        } catch (error) {
            console.error('Error uploading file:', error);
            // Handle error appropriately
        } finally {
            setIsLoading(false);
        }
    };

    const handleUrlGenerate = async (url: string) => {
        try {
            setIsLoading(true);
            // Implement URL-based generation here
            console.log('Generating from URL:', url);
        } catch (error) {
            console.error('Error generating from URL:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className='min-h-screen bg-gradient-to-b from-white to-gray-50'>
            <main className='container mx-auto px-4 py-16'>
                <div className='text-center mb-16'>
                    <h1 className='text-5xl font-bold mb-6'>
                        Instant <span className='text-green-500'>quizzes</span>
                    </h1>
                    <h2 className='text-3xl font-semibold mb-2'>
                        from <span className='text-orange-500'>PDFs</span> with{' '}
                        <span className='text-purple-500'>AI</span>
                    </h2>
                </div>

                <div className='space-y-8'>
                    <FileUpload onFileSelect={handleFileSelect} />
                    <div className='text-center text-gray-500'>or</div>
                    <UrlInput
                        onGenerate={handleUrlGenerate}
                        isLoading={isLoading}
                    />
                </div>
            </main>
        </div>
    );
}
