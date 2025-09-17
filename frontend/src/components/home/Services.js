export default function Services() {
  const services = [
    {
      title: 'Esame della Vista',
      description: 'Controlli professionali con strumentazioni all\'avanguardia',
      icon: '👁️',
    },
    {
      title: 'Lenti Progressive',
      description: 'Soluzioni innovative per ogni esigenza visiva',
      icon: '🔍',
    },
    {
      title: 'Riparazioni',
      description: 'Servizio rapido di riparazione per i tuoi occhiali',
      icon: '🔧',
    },
    {
      title: 'Consegna a Domicilio',
      description: 'Ricevi i tuoi prodotti direttamente a casa',
      icon: '🚚',
    },
  ]

  return (
    <div className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">I Nostri Servizi</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Professionalità e cura del dettaglio per offrirti sempre il meglio per la tua vista
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {services.map((service, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
              <div className="text-4xl mb-4">{service.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{service.title}</h3>
              <p className="text-gray-600">{service.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}