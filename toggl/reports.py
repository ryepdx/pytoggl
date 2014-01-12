from datetime import datetime, date

from goodcode import Dictionary
from .session import Session

__all__ = ['Reports']


class Reports(object):

    BASE_URL = 'https://toggl.com/reports/api/v2/'
    USER_AGENT = 'pytoggl/0.0; (info@dobarkod.hr)'
    REPORT_TYPES = ('weekly', 'details', 'summary')

    def __init__(self, api_token):
        self.workspace_id = None
        self.session = Session(self.BASE_URL, api_token)

    def for_workspace(self, workspace_id):
        r = Reports('-')
        r.session = self.session
        r.workspace_id = workspace_id
        return r

    def request(self, type, workspace_id=None, **params):
        if type not in self.REPORT_TYPES:
            raise ValueError('unsupported report type: ' + str(type))

        if workspace_id is None:
            if self.workspace_id is None:
                raise ValueError('missing workspace ID')
            workspace_id = self.workspace_id

        for k, v in params.iteritems():
            if isinstance(v, datetime) or isinstance(v, date):
                params[k] = v.strftime('%Y-%m-%d')

        params['workspace_id'] = workspace_id
        params['user_agent'] = self.USER_AGENT

        data = self.session.get(type, **params)
        return Dictionary(**data)

    @classmethod
    def _get_totals(cls, data):
        return Dictionary(
            grand=data.total_grand // 1000,
            grand_hm=cls._ms_to_hm(data.total_grand),
            billable=data.total_billable // 1000,
            billable_hm=cls._ms_to_hm(data.total_billable),
            currencies=data.total_currencies)

    @staticmethod
    def _ms_to_hm(val):
        minutes = val // 60000
        return u'%d:%02d' % (minutes // 60, minutes % 60)

    def weekly(self, **params):
        return self.request('weekly', **params)

    def details(self, **params):
        return self.request('details', **params)

    def summary(self, **params):
        data = self.request('summary', **params)

        def _get_title(t):
            if hasattr(t, 'project'):
                return t.project
            elif hasattr(t, 'client'):
                return t.client
            elif hasattr(t, 'user'):
                return t.user
            elif hasattr(t, 'task'):
                return t.task
            elif hasattr(t, 'time_entry'):
                return t.time_entry
            else:
                return ''

        groups = []

        for group_data in data.data:
            subgroups = []
            for subgroup_data in group_data.items:
                subgroups.append(Dictionary(
                    _unicode_value=_get_title(subgroup_data.title),
                    title=_get_title(subgroup_data.title),
                    time=subgroup_data.time // 1000,
                    time_hm=self._ms_to_hm(subgroup_data.time),
                    currency=subgroup_data.cur,
                    amount=subgroup_data.sum,
                    rate=subgroup_data.rate))
            groups.append(Dictionary(
                _unicode_value=_get_title(group_data.title),
                id=group_data.id,
                title=_get_title(group_data.title),
                time=group_data.time // 1000,
                time_hm=self._ms_to_hm(group_data.time),
                currencies=group_data.total_currencies,
                subgroups=subgroups))

        return Dictionary(total=self._get_totals(data), groups=groups)
