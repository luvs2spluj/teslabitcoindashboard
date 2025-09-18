'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export function TeslaEnergy() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Energy Business Overview</CardTitle>
          <CardDescription>
            Solar and storage capacity and revenue trends
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[400px] flex items-center justify-center text-muted-foreground">
            Energy business overview chart
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Solar Capacity</CardTitle>
            <CardDescription>
              Solar MW deployed quarterly
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center text-muted-foreground">
              Solar capacity chart
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Storage Capacity</CardTitle>
            <CardDescription>
              Storage MWh deployed quarterly
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center text-muted-foreground">
              Storage capacity chart
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
