import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { TeslaOverview } from '@/components/charts/tesla-overview'
import { TeslaVehicles } from '@/components/charts/tesla-vehicles'
import { TeslaEnergy } from '@/components/charts/tesla-energy'
import { TeslaMargins } from '@/components/charts/tesla-margins'
import { TeslaScenarios } from '@/components/charts/tesla-scenarios'

export default function TeslaPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Tesla Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Comprehensive analysis of Tesla's business metrics, financial performance, and market scenarios.
        </p>
      </div>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="vehicles">Vehicles</TabsTrigger>
          <TabsTrigger value="energy">Energy</TabsTrigger>
          <TabsTrigger value="margins">Margins</TabsTrigger>
          <TabsTrigger value="scenarios">Scenarios</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <TeslaOverview />
        </TabsContent>

        <TabsContent value="vehicles" className="space-y-6">
          <TeslaVehicles />
        </TabsContent>

        <TabsContent value="energy" className="space-y-6">
          <TeslaEnergy />
        </TabsContent>

        <TabsContent value="margins" className="space-y-6">
          <TeslaMargins />
        </TabsContent>

        <TabsContent value="scenarios" className="space-y-6">
          <TeslaScenarios />
        </TabsContent>
      </Tabs>
    </div>
  )
}
