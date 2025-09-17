'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useDispatch, useSelector } from 'react-redux'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { loginUser } from '@/store/slices/authSlice'
import Link from 'next/link'

export default function LoginForm() {
  const router = useRouter()
  const dispatch = useDispatch()
  const { loading, error } = useSelector((state) => state.auth)
  
  const { register, handleSubmit, formState: { errors } } = useForm()

  const onSubmit = async (data) => {
    try {
      const result = await dispatch(loginUser(data))
      if (result.type === 'auth/login/fulfilled') {
        toast.success('Login effettuato con successo!')
        router.push('/')
      } else {
        toast.error(result.payload || 'Errore durante il login')
      }
    } catch (error) {
      toast.error('Errore durante il login')
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Accedi al tuo Account</h2>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
              Username o Email
            </label>
            <input
              id="username"
              type="text"
              className="input-field"
              {...register('username', { required: 'Username richiesto' })}
            />
            {errors.username && (
              <p className="text-red-500 text-sm mt-1">{errors.username.message}</p>
            )}
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              className="input-field"
              {...register('password', { required: 'Password richiesta' })}
            />
            {errors.password && (
              <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>
            )}
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary disabled:opacity-50"
          >
            {loading ? 'Accesso in corso...' : 'Accedi'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Non hai un account?{' '}
            <Link href="/registrati" className="text-primary-600 hover:text-primary-700 font-medium">
              Registrati qui
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}