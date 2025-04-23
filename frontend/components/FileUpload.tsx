'use client';

import type React from 'react';

import { useState, useRef, useEffect } from 'react';
import {
    Upload,
    FileUp,
    AlertCircle,
    Loader2,
    CheckCircle2,
    Sparkles,
    LinkIcon,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

export function FileUpload() {
    const [isDragging, setIsDragging] = useState(false);
    const [file, setFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);
    const [urlInput, setUrlInput] = useState('');
    const [uploadProgress, setUploadProgress] = useState(0);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const MAX_FILE_SIZE = 25 * 1024 * 1024; // 25MB

    useEffect(() => {
        if (isUploading) {
            const interval = setInterval(() => {
                setUploadProgress((prev) => {
                    if (prev >= 100) {
                        clearInterval(interval);
                        return 100;
                    }
                    return prev + 5;
                });
            }, 100);

            return () => clearInterval(interval);
        } else {
            setUploadProgress(0);
        }
    }, [isUploading]);

    const handleDragEnter = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    };

    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const validateFile = (file: File): boolean => {
        setError(null);

        // Check file type
        if (!file.type.includes('pdf')) {
            setError('Please upload a PDF file');
            return false;
        }

        // Check file size
        if (file.size > MAX_FILE_SIZE) {
            setError('File size exceeds 25MB limit');
            return false;
        }

        return true;
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);

        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile && validateFile(droppedFile)) {
            setFile(droppedFile);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0];
            if (validateFile(selectedFile)) {
                setFile(selectedFile);
            }
        }
    };

    const handleButtonClick = () => {
        fileInputRef.current?.click();
    };

    const handleGenerate = () => {
        if (file || urlInput) {
            setIsUploading(true);
            setError(null);

            // Simulate upload process
            setTimeout(() => {
                setIsUploading(false);
                setIsSuccess(true);

                // Reset success state after 2 seconds
                setTimeout(() => {
                    setIsSuccess(false);
                }, 2000);
            }, 2500);
        } else {
            setError('Please upload a PDF file or enter a URL');
        }
    };

    const handleRemoveFile = () => {
        setFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div className='w-full space-y-6'>
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className={cn(
                    'border-2 border-dashed rounded-2xl p-10 transition-all duration-300 ease-in-out shadow-lg backdrop-blur-sm',
                    isDragging
                        ? 'border-emerald-400 bg-emerald-50/80 dark:bg-emerald-950/30'
                        : 'border-slate-200 dark:border-slate-700/50',
                    file
                        ? 'bg-white/80 dark:bg-slate-800/50'
                        : 'bg-white/60 dark:bg-slate-900/40'
                )}
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
            >
                <AnimatePresence mode='wait'>
                    {file ? (
                        <motion.div
                            key='file-preview'
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            className='w-full'
                        >
                            <div className='flex items-center justify-between p-4 bg-gradient-to-r from-slate-50 to-blue-50 dark:from-slate-800 dark:to-blue-900/20 rounded-xl border border-slate-200 dark:border-slate-700/50 shadow-sm'>
                                <div className='flex items-center space-x-4'>
                                    <div className='p-3 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-lg shadow-md'>
                                        <FileUp className='h-6 w-6 text-white' />
                                    </div>
                                    <div className='flex flex-col'>
                                        <span className='text-base font-medium truncate max-w-[200px] sm:max-w-xs'>
                                            {file.name}
                                        </span>
                                        <span className='text-xs text-slate-500 dark:text-slate-400'>
                                            {(
                                                file.size /
                                                (1024 * 1024)
                                            ).toFixed(2)}{' '}
                                            MB • PDF
                                        </span>
                                    </div>
                                </div>
                                <Button
                                    variant='ghost'
                                    size='sm'
                                    onClick={handleRemoveFile}
                                    className='text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full h-8 w-8 p-0'
                                >
                                    <span className='sr-only'>Remove file</span>
                                    <svg
                                        xmlns='http://www.w3.org/2000/svg'
                                        width='16'
                                        height='16'
                                        viewBox='0 0 24 24'
                                        fill='none'
                                        stroke='currentColor'
                                        strokeWidth='2'
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                    >
                                        <path d='M18 6 6 18'></path>
                                        <path d='m6 6 12 12'></path>
                                    </svg>
                                </Button>
                            </div>
                        </motion.div>
                    ) : (
                        <motion.div
                            key='upload-area'
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className='flex flex-col items-center justify-center space-y-6'
                        >
                            <motion.div
                                className='relative p-6 bg-gradient-to-br from-violet-500 to-purple-600 rounded-full shadow-lg'
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                <Upload className='h-10 w-10 text-white' />
                                <span className='absolute -right-1 -top-1 flex h-6 w-6 items-center justify-center rounded-full bg-white text-xs font-bold text-violet-600'>
                                    PDF
                                </span>
                            </motion.div>
                            <div className='text-center space-y-2'>
                                <h3 className='text-xl font-semibold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent'>
                                    Drag & drop to upload
                                </h3>
                                <p className='text-sm text-slate-500 dark:text-slate-400'>
                                    .pdf • Max 25MB
                                </p>
                            </div>
                            <Button
                                variant='outline'
                                onClick={handleButtonClick}
                                className='mt-2 border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-800/80 hover:bg-slate-100 dark:hover:bg-slate-700 backdrop-blur-sm transition-all duration-300 px-6 py-5 h-auto text-base font-medium shadow-sm'
                            >
                                Choose file
                            </Button>
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.div>

            <AnimatePresence>
                {error && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className='flex items-center space-x-2 text-red-600 dark:text-red-500 text-sm bg-red-50 dark:bg-red-900/20 p-3 rounded-lg'
                    >
                        <AlertCircle className='h-4 w-4' />
                        <span>{error}</span>
                    </motion.div>
                )}
            </AnimatePresence>

            <div className='flex items-center justify-center space-x-4'>
                <div className='h-px bg-gradient-to-r from-transparent via-slate-300 dark:via-slate-700 to-transparent w-full max-w-[100px]'></div>
                <span className='text-slate-500 dark:text-slate-400 text-sm font-medium'>
                    or
                </span>
                <div className='h-px bg-gradient-to-r from-transparent via-slate-300 dark:via-slate-700 to-transparent w-full max-w-[100px]'></div>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className='flex flex-col sm:flex-row gap-3'
            >
                <div className='relative flex-1'>
                    <div className='absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none'>
                        <LinkIcon className='h-5 w-5 text-slate-400' />
                    </div>
                    <Input
                        type='text'
                        placeholder='Paste any website link or PDF URL'
                        value={urlInput}
                        onChange={(e) => setUrlInput(e.target.value)}
                        className='pl-10 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border-slate-200 dark:border-slate-700 h-12 text-base shadow-sm'
                    />
                </div>
                <Button
                    onClick={handleGenerate}
                    className={cn(
                        'h-12 px-6 text-base font-medium shadow-md transition-all duration-300',
                        isSuccess
                            ? 'bg-emerald-500 hover:bg-emerald-600'
                            : 'bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700'
                    )}
                    disabled={isUploading}
                >
                    {isUploading ? (
                        <>
                            <Loader2 className='mr-2 h-5 w-5 animate-spin' />
                            Processing...
                        </>
                    ) : isSuccess ? (
                        <>
                            <CheckCircle2 className='mr-2 h-5 w-5' />
                            Success!
                        </>
                    ) : (
                        <>
                            <Sparkles className='mr-2 h-5 w-5' />
                            Generate
                            <span className='ml-2 inline-flex items-center justify-center rounded-full bg-white/20 w-6 h-6 text-xs font-bold'>
                                5
                            </span>
                        </>
                    )}
                </Button>
            </motion.div>

            <AnimatePresence>
                {isUploading && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className='w-full'
                    >
                        <div className='w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden'>
                            <div
                                className='h-full bg-gradient-to-r from-violet-500 to-indigo-600 transition-all duration-300 rounded-full'
                                style={{ width: `${uploadProgress}%` }}
                            />
                        </div>
                        <div className='flex justify-between text-xs text-slate-500 dark:text-slate-400 mt-1'>
                            <span>Processing PDF...</span>
                            <span>{uploadProgress}%</span>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <input
                type='file'
                ref={fileInputRef}
                onChange={handleFileChange}
                accept='.pdf'
                className='hidden'
            />
        </div>
    );
}
