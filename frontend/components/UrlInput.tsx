import { useState } from 'react';

interface UrlInputProps {
    onGenerate: (url: string) => void;
    isLoading?: boolean;
}

export default function UrlInput({
    onGenerate,
    isLoading = false,
}: UrlInputProps) {
    const [url, setUrl] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (url.trim()) {
            onGenerate(url.trim());
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            className='w-full max-w-2xl mx-auto flex gap-2'
        >
            <input
                type='text'
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder='Paste any website link or upload a file'
                className='flex-1 px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-400'
            />
            <button
                type='submit'
                disabled={isLoading || !url.trim()}
                className={`px-6 py-2 rounded-lg bg-purple-500 text-white font-medium flex items-center gap-2
                    ${
                        isLoading || !url.trim()
                            ? 'opacity-50 cursor-not-allowed'
                            : 'hover:bg-purple-600'
                    }`}
            >
                Generate
                {isLoading ? (
                    <span className='inline-block animate-spin'>⚡</span>
                ) : (
                    <span>⚡</span>
                )}
                <span className='ml-1'>5</span>
            </button>
        </form>
    );
}
