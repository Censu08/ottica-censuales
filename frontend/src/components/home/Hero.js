import Link from 'next/link'

export default function Hero() {
  return (
    <div className="relative bg-gradient-to-r from-primary-600 to-primary-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            La Tua Vista è la Nostra Missione
          </h1>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Scopri la nostra selezione di occhiali da vista e da sole delle migliori marche. 
            Qualità, stile e professionalità da oltre 30 anni.
          </p>
          <div className="space-x-4">
            <Link href="/prodotti" className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Scopri i Prodotti
            </Link>
            <Link href="/negozi" className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary-600 transition-colors">
              Trova il Negozio
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}