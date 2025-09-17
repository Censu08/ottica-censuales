import Layout from '@/components/layout/Layout'
import Hero from '@/components/home/Hero'
import FeaturedProducts from '@/components/home/FeaturedProducts'
import Services from '@/components/home/Services'

export default function HomePage() {
  return (
    <Layout>
      <Hero />
      <FeaturedProducts />
      <Services />
    </Layout>
  )
}