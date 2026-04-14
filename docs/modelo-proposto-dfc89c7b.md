<!-- title: Modelo Proposto | url: https://outline.seazone.com.br/doc/modelo-proposto-IizQMGe67Y | area: Tecnologia -->

# Modelo Proposto

```yaml
Amenities
    - id            int
    - name          string
    - condition     string
    - category      string
    - active        bool

Property_Amenities
    - property_id   int
    - amenity_id    int
    
Property_Extra_Amenities
    - id            int
    - property_id   int
    - name          string
    - condition     string
    - details       string
    - active        bool
```