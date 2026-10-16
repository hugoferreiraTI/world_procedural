"""Identidade institucional tipada; os aliases exclusivos mantêm consumidores antigos."""


def organization_id(context, kind):
    if context.get('organization_type'):
        return context.get('organization_id') if context['organization_type']==kind else None
    # Fixtures/programas legados só são aceitos quando a referência é inequívoca.
    if context.get('group_id') is not None and context.get('faction_id') is not None:
        return None
    return context.get(kind+'_id')


def bind_organization(context, kind, entity_id):
    context.pop('group_id',None);context.pop('faction_id',None)
    context.update(organization_type=kind,organization_id=entity_id)
    context[kind+'_id']=entity_id
