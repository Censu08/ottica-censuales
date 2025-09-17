export default function ProductCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden animate-pulse">
      <div className="aspect-square bg-gray-300" />
      <div className="p-4 space-y-3">
        <div className="h-4 bg-gray-300 rounded w-1/3" />
        <div className="h-5 bg-gray-300 rounded w-3/4" />
        <div className="h-4 bg-gray-300 rounded w-full" />
        <div className="flex justify-between items-center">
          <div className="h-6 bg-gray-300 rounded w-1/4" />
          <div className="h-8 w-8 bg-gray-300 rounded-full" />
        </div>
      </div>
    </div>
  )
}