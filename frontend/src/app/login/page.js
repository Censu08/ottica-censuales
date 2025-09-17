import Layout from '@/components/layout/Layout'
import LoginForm from '@/components/auth/LoginForm'

export default function LoginPage() {
  return (
    <Layout>
      <div className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <LoginForm />
        </div>
      </div>
    </Layout>
  )
}