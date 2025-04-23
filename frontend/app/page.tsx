import { FileUpload } from '@/components/FileUpload';

export default function Home() {
    return (
        <main className='min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-slate-50 via-purple-50 to-blue-50 dark:from-slate-950 dark:via-purple-950/20 dark:to-blue-950/20'>
            <div className='absolute inset-0 overflow-hidden pointer-events-none'>
                <div className='absolute -top-[40%] -right-[10%] w-[70%] h-[70%] bg-gradient-to-br from-purple-200/20 to-blue-300/20 dark:from-purple-900/20 dark:to-blue-800/20 rounded-full blur-3xl' />
                <div className='absolute -bottom-[40%] -left-[10%] w-[70%] h-[70%] bg-gradient-to-tr from-emerald-200/20 to-teal-300/20 dark:from-emerald-900/20 dark:to-teal-800/20 rounded-full blur-3xl' />
            </div>

            <div className='max-w-3xl w-full mx-auto text-center space-y-6 relative z-10'>
                <div className='space-y-2 mb-8'>
                    <h1 className='text-5xl md:text-6xl font-bold tracking-tight bg-gradient-to-r from-purple-600 via-emerald-500 to-blue-600 text-transparent bg-clip-text'>
                        Instant <span className='font-extrabold'>quizzes</span>
                    </h1>
                    <p className='text-2xl md:text-3xl font-medium'>
                        from{' '}
                        <span className='text-orange-500 font-semibold'>
                            PDFs
                        </span>{' '}
                        with{' '}
                        <span className='text-violet-600 dark:text-violet-400 font-semibold'>
                            AI
                        </span>
                    </p>
                </div>

                <div className='mt-8 transform transition-all duration-500 hover:scale-[1.01]'>
                    <FileUpload />
                </div>

                <p className='text-sm text-slate-500 dark:text-slate-400 mt-12 max-w-md mx-auto'>
                    Upload your study materials and get AI-generated quizzes in
                    seconds. Perfect for students, teachers, and lifelong
                    learners.
                </p>
            </div>
        </main>
    );
}
