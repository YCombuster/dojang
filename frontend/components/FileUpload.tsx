import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import Image from 'next/image';

interface FileUploadProps {
    onFileSelect: (file: File) => void;
}

export default function FileUpload({ onFileSelect }: FileUploadProps) {
    const onDrop = useCallback(
        (acceptedFiles: File[]) => {
            if (acceptedFiles?.[0]) {
                onFileSelect(acceptedFiles[0]);
            }
        },
        [onFileSelect]
    );

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
        },
        maxSize: 25 * 1024 * 1024, // 25MB
        multiple: false,
    });

    return (
        <div className='w-full max-w-2xl mx-auto'>
            <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
                    ${
                        isDragActive
                            ? 'border-purple-400 bg-purple-50'
                            : 'border-gray-300 hover:border-gray-400'
                    }`}
            >
                <input {...getInputProps()} />
                <div className='flex flex-col items-center gap-2'>
                    <Image
                        src='/upload-icon.svg'
                        alt='Upload'
                        width={40}
                        height={40}
                        className='opacity-50'
                    />
                    <p className='text-lg text-gray-600'>
                        Drag & drop to upload
                    </p>
                    <p className='text-sm text-gray-500'>.pdf • Max 25MB</p>
                    <button
                        type='button'
                        className='mt-4 px-6 py-2 bg-gray-100 hover:bg-gray-200 rounded-md text-gray-700'
                    >
                        Choose file
                    </button>
                </div>
            </div>
        </div>
    );
}
